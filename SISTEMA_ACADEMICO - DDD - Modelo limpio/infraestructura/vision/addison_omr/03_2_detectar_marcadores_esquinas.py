"""Etapa 03.2: localización OBSERVADA de los cuatro cuadrados negros.

Se buscan primero en una foto rectificada por ORB/SIFT. A diferencia de
proyectar coordenadas, esta función comprueba la existencia de tinta cuadrada.
No acepta formas difusas ni inventa puntos para las esquinas ausentes.
"""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import cv2
import numpy as np

from .definir_parametros_omr import Imagen


# ETAPA 03.2 — Detecta realmente los cuadrados negros, con varios umbrales.
def detectar_marcadores(
    gris: Imagen, coordenadas: Mapping[str, Any], radio_busqueda: int = 39,
) -> tuple[dict[str, list[float]], dict[str, Any]]:
    """Encuentra centros por componentes compactas próximas a cada ancla.

    Devuelve (centros_observados, diagnóstico). Solo se usa para registros
    de hoja ya aproximados; la detección no es una búsqueda global arbitraria.
    """
    encontrados: dict[str, list[float]] = {}
    detalles: dict[str, Any] = {}
    for nombre, posicion in coordenadas.items():
        x, y = (int(round(float(valor))) for valor in posicion)
        x0, y0 = max(0, x-radio_busqueda), max(0, y-radio_busqueda)
        x1 = min(gris.shape[1], x + radio_busqueda + 1)
        y1 = min(gris.shape[0], y + radio_busqueda + 1)
        if x1 <= x0 or y1 <= y0:
            detalles[nombre] = {"encontrado": False, "motivo": "fuera_de_imagen"}
            continue
        region = cv2.GaussianBlur(gris[y0:y1, x0:x1], (3, 3), 0)
        candidatos = []
        for umbral in (90, 115, 140, 165, 190, 215):
            _, mascara = cv2.threshold(region, umbral, 255, cv2.THRESH_BINARY_INV)
            mascara = cv2.morphologyEx(
                mascara, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8)
            )
            total, _, componentes, centros = cv2.connectedComponentsWithStats(mascara)
            for indice in range(1, total):
                _, _, ancho, alto, area = (int(v) for v in componentes[indice])
                if not (12 <= ancho <= 32 and 12 <= alto <= 32
                        and 110 <= area <= 850 and 0.77 <= ancho / alto <= 1.30
                        and area / (ancho * alto) > 0.62):
                    continue
                cx, cy = centros[indice] + [x0, y0]
                distancia = float(np.hypot(cx - x, cy - y))
                if distancia > 26:
                    continue
                compacidad = area / (ancho * alto)
                puntuacion = (distancia/8 + abs(ancho-20)/7 + abs(alto-20)/7
                              + max(0, .80-compacidad)*4)
                candidatos.append((puntuacion, float(cx), float(cy), umbral))
        if not candidatos:
            detalles[nombre] = {
                "encontrado": False, "motivo": "cuadrado_no_localizado",
                "posicion_esperada_px": [x, y],
            }
            continue
        _, cx, cy, umbral = min(candidatos)
        encontrados[nombre] = [round(cx, 3), round(cy, 3)]
        detalles[nombre] = {
            "encontrado": True, "centro_observado_px": encontrados[nombre],
            "distancia_a_estimacion_px": round(float(np.hypot(cx-x, cy-y)), 2),
            "umbral_utilizado": umbral,
        }
    return encontrados, detalles


# PASO 3.8 — Rectifica perspectiva según cuadrados físicos, no esquinas estimadas.
def refinar_con_marcadores(
    foto_gris: Imagen, plantilla_gris: Imagen, homografia: Imagen,
    coordenadas: Mapping[str, Any],
) -> tuple[Imagen | None, dict[str, Any]]:
    """Propone una homografía refinada con 3 o 4 cuadrados observados.

    La corrección nunca debe aceptarse por sí sola: la etapa 3.10 compara
    también la homografía ORB/SIFT original sobre la cuadrícula interior.
    """
    # Las plantillas ADDISON usan nombres descriptivos; las rutinas de
    # refinamiento emplean tl/tr/bl/br. Normalizar sin cambiar el JSON original.
    nombres = {
        "tl": "superior_izquierda", "tr": "superior_derecha",
        "bl": "inferior_izquierda", "br": "inferior_derecha",
    }
    coordenadas = {
        corto: coordenadas[corto] if corto in coordenadas
                else coordenadas[largo]
        for corto, largo in nombres.items()
        if corto in coordenadas or largo in coordenadas
    }
    claves = ("tl", "tr", "bl", "br")
    if not all(clave in coordenadas for clave in claves):
        return None, {"valido": False, "motivo": "Faltan coordenadas de los cuatro marcadores en plantilla"}
    esperados, diag_plantilla = detectar_marcadores(plantilla_gris, coordenadas)
    if len(esperados) != 4:
        return None, {"valido": False, "motivo": "Marcadores no legibles en plantilla maestra",
                      "marcadores_plantilla": diag_plantilla}
    h, w = plantilla_gris.shape
    aproximada = cv2.warpPerspective(
        foto_gris, np.linalg.inv(homografia), (w, h),
        borderMode=cv2.BORDER_CONSTANT, borderValue=255,
    )
    observados, diag_foto = detectar_marcadores(aproximada, coordenadas)
    info: dict[str, Any] = {
        "valido": False, "marcadores_detectados": len(observados),
        "marcadores_rectificados": diag_foto,
        "marcadores_plantilla": esperados,
    }
    # Respaldo de alta certeza: si un cuadrado se fusiona con el borde impreso,
    # la segmentación por componentes falla. Correlacionamos entonces la
    # impresión del propio cuadrado físico (+/-23 px), sin inventar coordenadas.
    # Requerimos una coincidencia fuerte del dibujo real de la plantilla.
    for clave in claves:
        if clave in observados:
            continue
        px, py = [int(round(float(v))) for v in coordenadas[clave]]
        mitad, margen = 12, 23
        if (px-mitad-margen < 0 or py-mitad-margen < 0
                or px+mitad+margen >= w or py+mitad+margen >= h):
            continue
        patron = plantilla_gris[py-mitad:py+mitad+1, px-mitad:px+mitad+1]
        roi = aproximada[py-mitad-margen:py+mitad+margen+1,
                         px-mitad-margen:px+mitad+margen+1]
        mapa = cv2.matchTemplate(
            cv2.GaussianBlur(roi, (3, 3), 0),
            cv2.GaussianBlur(patron, (3, 3), 0),
            cv2.TM_CCOEFF_NORMED,
        )
        _, puntuacion, _, (xx, yy) = cv2.minMaxLoc(mapa)
        info["marcadores_rectificados"][clave]["correlacion_respaldo"] = round(float(puntuacion), 3)
        if puntuacion < .80:
            continue
        delta = np.float32([xx-margen, yy-margen])
        centro = np.float32(esperados[clave]) + delta
        observados[clave] = np.round(centro, 3).tolist()
        info["marcadores_rectificados"][clave] = {
            "encontrado": True, "centro_observado_px": observados[clave],
            "metodo": "coincidencia_visual_cuadrado",
            "correlacion": round(float(puntuacion), 3),
        }
    info["marcadores_detectados"] = len(observados)
    if len(observados) < 3:
        # ORB/SIFT puede funcionar aun sin cuadrados suficientes.
        # Esta función NO es la verificación final de la alineación.
        info["motivo"] = "Menos de tres marcadores; probar ORB/SIFT sin correccion"
        return None, info
    visibles = [clave for clave in claves if clave in observados]
    origen = np.float32([observados[clave] for clave in visibles])
    destino = np.float32([esperados[clave] for clave in visibles])
    if len(visibles) == 4:
        correccion = cv2.getPerspectiveTransform(origen, destino)
        info["metodo_correccion"] = "perspectiva_cuatro_marcadores"
    else:
        # Con tres puntos sólo puede determinarse una transformación afín;
        # nunca inferimos una perspectiva completa desde tres esquinas.
        af = cv2.getAffineTransform(origen, destino)
        correccion = np.vstack([af, [0, 0, 1]])
        info["metodo_correccion"] = "afin_tres_marcadores"
        singular = np.linalg.svd(af[:, :2], compute_uv=False)
        if singular.min() < .94 or singular.max() > 1.06:
            info["motivo"] = "Afin de tres marcadores implica deformación excesiva"
            return None, info
    desplazamientos = cv2.perspectiveTransform(
        np.float32([[[w*0.10, h*0.10]], [[w*0.90, h*0.10]],
                    [[w*0.10, h*0.90]], [[w*0.90, h*0.90]]]),
        correccion,
    ).reshape(-1, 2)
    puntos = np.float32([[w*.10, h*.10], [w*.90, h*.10],
                         [w*.10, h*.90], [w*.90, h*.90]])
    magnitudes = np.linalg.norm(desplazamientos - puntos, axis=1)
    info["correccion_maxima_px"] = round(float(magnitudes.max()), 2)
    # Rechazar cambios geométricos grandes derivados de anclas equivocadas.
    if not np.isfinite(correccion).all() or float(magnitudes.max()) > 30:
        info["motivo"] = "La corrección por marcadores excede los límites geométricos"
        return None, info
    homografia_final = homografia @ np.linalg.inv(correccion)
    if not np.isfinite(homografia_final).all():
        info["motivo"] = "Homografía refinada no finita"
        return None, info
    # Transformación de los centros físicamente observados a la fotografía original.
    coords_raw = cv2.perspectiveTransform(origen.reshape(-1, 1, 2), homografia).reshape(-1, 2)
    info["marcadores_foto_original_px"] = {
        clave: np.round(coords_raw[i], 2).tolist() for i, clave in enumerate(visibles)
    }
    info["valido"] = True
    info["motivo"] = "Ajuste propuesto con cuadrados; requiere validar cuadrícula"
    return homografia_final, info


# PASO 3.10 — Hipótesis adicionales al detectar cuatro cuadrados contradictorios.
def hipotesis_tres_de_cuatro(
    homografia: Imagen, info: Mapping[str, Any], ancho: int, alto: int,
) -> list[tuple[str, Imagen]]:
    """Prueba excluir cada ancla; una ancla falsa no arrastra toda la hoja.

    Estas son HIPÓTESIS, no resultados seguros. Cada una requiere superar
    la validación independiente de la cuadrícula interior.
    """
    observaciones = info.get("marcadores_rectificados", {})
    referencia = info.get("marcadores_plantilla", {})
    visibles = [clave for clave in ("tl", "tr", "bl", "br")
                if observaciones.get(clave, {}).get("encontrado") and clave in referencia]
    if len(visibles) != 4:
        return []
    salida = []
    puntos_control = np.float32([[ancho*.1, alto*.1], [ancho*.9, alto*.1],
                                [ancho*.1, alto*.9], [ancho*.9, alto*.9]])
    for omitido in visibles:
        claves = [clave for clave in visibles if clave != omitido]
        origen = np.float32([observaciones[c]["centro_observado_px"] for c in claves])
        destino = np.float32([referencia[c] for c in claves])
        afin = cv2.getAffineTransform(origen, destino)
        if not np.isfinite(afin).all():
            continue
        singular = np.linalg.svd(afin[:, :2], compute_uv=False)
        if singular.min() < .94 or singular.max() > 1.06:
            continue
        cor = np.vstack((afin, [0., 0., 1.]))
        cambiados = cv2.perspectiveTransform(puntos_control.reshape(-1, 1, 2), cor).reshape(-1, 2)
        if float(np.max(np.linalg.norm(cambiados-puntos_control, axis=1))) > 24:
            continue
        try:
            H = homografia @ np.linalg.inv(cor)
        except np.linalg.LinAlgError:
            continue
        if np.isfinite(H).all():
            salida.append((f"afin_tres_sin_{omitido}", H))
    return salida

"""Registro geométrico ORB/SIFT, validación de homografía y refinamiento ECC."""

# ===================================================================
# MAPA DE REVISIÓN: pasos 3.1, 3.2, 3.3, 3.4, 3.5, 3.6
# Consulta 00_LEER_SECUENCIA.md para recorrer el algoritmo en orden.
# La numeración es documental; no cambia llamadas ni nombres Python.
# ===================================================================


from __future__ import annotations

from typing import Any
from collections.abc import Mapping
from pathlib import Path
import cv2
import json
import numpy as np
from .definir_parametros_omr import Diccionario, ESCALA_ECC, Imagen
from .localizar_burbujas import _centro, _iterar_burbujas
from .cargar_plantilla_referencia import _leer_imagen, guardar_json, _ruta_coordenadas
from .detectar_marcadores_esquinas import refinar_con_marcadores, hipotesis_tres_de_cuatro
from .validar_cuadricula_respuestas import verificar_cuadricula
from .corregir_alineacion_local import corregir_cuadricula_local


# PASO 3.6 — Refina una imagen ya alineada; solo con --refinar-ecc.
def mejora_ecc(
    imagen_gris: Imagen, referencia: Imagen, datos: Mapping[str, Any]
) -> tuple[Imagen, Diccionario]:
    """Refina una imagen YA alineada mediante una transformación afín pequeña.

    Se excluyen las burbujas del ajuste para evitar que las marcas modifiquen
    la transformación calculada. Si el ajuste es dudoso, devuelve la imagen
    original junto con una explicación.
    """
    mascara = np.full(referencia.shape, 255, dtype=np.uint8)
    for burbuja in _iterar_burbujas(datos):
        cv2.circle(
            mascara,
            _centro(burbuja),
            round(burbuja["radio_px"] * 1.08),
            0,
            -1,
        )

    mascara[:30, :] = 0
    mascara[-25:, :] = 0

    def reducir(imagen: Imagen) -> Imagen:
        return cv2.resize(
            imagen,
            None,
            fx=ESCALA_ECC,
            fy=ESCALA_ECC,
            interpolation=cv2.INTER_AREA,
        )

    matriz = np.eye(2, 3, dtype=np.float32)
    criterios = (
        cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,
        100,
        1e-5,
    )
    try:
        correlacion, matriz = cv2.findTransformECC(
            reducir(referencia).astype(np.float32) / 255.0,
            reducir(imagen_gris).astype(np.float32) / 255.0,
            matriz,
            cv2.MOTION_AFFINE,
            criterios,
            reducir(mascara),
            5,
        )
    except cv2.error as error:
        return imagen_gris, {"aplicado": False, "motivo": str(error)[:200]}

    matriz[:, 2] /= ESCALA_ECC
    desplazamiento_maximo = float(np.max(np.abs(matriz[:, 2])))
    deformacion_maxima = float(
        np.max(np.abs(matriz[:, :2] - np.eye(2)))
    )
    if (
        correlacion < 0.70
        or desplazamiento_maximo > 10
        or deformacion_maxima > 0.025
    ):
        return imagen_gris, {
            "aplicado": False,
            "correlacion": round(float(correlacion), 4),
            "motivo": "correccion ECC fuera de limites geometricos",
        }

    imagen_corregida = cv2.warpAffine(
        imagen_gris,
        matriz,
        (imagen_gris.shape[1], imagen_gris.shape[0]),
        flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=255,
    )
    return imagen_corregida, {
        "aplicado": True,
        "correlacion": round(float(correlacion), 4),
        "matriz": np.round(matriz, 5).tolist(),
    }


# PASO 3.4 — Comprueba cobertura, forma y error de homografía.
def medidas_homografia(
    H: Imagen | None,
    puntos_plantilla: Imagen,
    buenos: Mapping[str, Imagen],
    inliers: Imagen | None,
    w: int,
    h: int,
    w_img: int,
    h_img: int,
) -> Diccionario | None:
    """Valida geometría y cobertura antes de aceptar una homografía."""
    if H is None or inliers is None:
        return None

    mascara = inliers.ravel() != 0
    cantidad = int(mascara.sum())
    if cantidad < 30:
        return None

    esquinas = np.float32(
        [[0, 0], [w - 1, 0], [w - 1, h - 1], [0, h - 1]]
    ).reshape(-1, 1, 2)
    proyectadas = cv2.perspectiveTransform(esquinas, H).reshape(-1, 2)
    if not np.isfinite(proyectadas).all():
        return None
    if not cv2.isContourConvex(proyectadas.astype(np.float32)):
        return None

    superficie = abs(cv2.contourArea(proyectadas.astype(np.float32)))
    ratio_superficie = superficie / (w_img * h_img)
    if not 0.12 <= ratio_superficie <= 3.0:
        return None

    longitudes = [
        float(np.linalg.norm(proyectadas[i] - proyectadas[(i + 1) % 4]))
        for i in range(4)
    ]
    if min(longitudes) < min(w_img, h_img) * 0.25:
        return None

    puntos_compatibles = puntos_plantilla[mascara]
    cobertura_ancho = float(
        (puntos_compatibles[:, 0].max() - puntos_compatibles[:, 0].min()) / w
    )
    cobertura_alto = float(
        (puntos_compatibles[:, 1].max() - puntos_compatibles[:, 1].min()) / h
    )
    envolvente = cv2.convexHull(puntos_compatibles.astype(np.float32))
    cobertura_convexa = float(cv2.contourArea(envolvente)) / (w * h)
    if (
        cobertura_ancho < 0.50
        or cobertura_alto < 0.48
        or cobertura_convexa < 0.18
    ):
        return None

    proporcion_inliers = cantidad / len(buenos["src"])
    if proporcion_inliers < 0.25:
        return None

    puntos_foto = buenos["dst"][mascara]
    puntos_proyectados = cv2.perspectiveTransform(
        puntos_compatibles.reshape(-1, 1, 2), H
    ).reshape(-1, 2)
    error_mediano = float(
        np.median(np.linalg.norm(puntos_proyectados - puntos_foto, axis=1))
    )
    if error_mediano > 4.0:
        return None

    return {
        "inliers": cantidad,
        "coincidencias_iniciales": len(buenos["src"]),
        "proporcion_inliers": round(proporcion_inliers, 4),
        "cobertura_ancho_plantilla": round(cobertura_ancho, 4),
        "cobertura_alto_plantilla": round(cobertura_alto, 4),
        "cobertura_convexa_plantilla": round(cobertura_convexa, 4),
        "area_documento_respecto_foto": round(ratio_superficie, 4),
        "error_mediano_px": round(error_mediano, 3),
        "esquinas_en_fotografia_px": np.round(proyectadas, 1).tolist(),
    }


# PASO 3.3 — Detecta y empareja rasgos para estimar homografía.
def extraer_coincidencias(
    template: Imagen, foto: Imagen, metodo: str
) -> tuple[Imagen, dict[str, Imagen], Imagen] | None:
    """Calcula coincidencias y una homografía desde la plantilla a la foto."""
    if metodo == "ORB":
        detector = cv2.ORB_create(
            nfeatures=8500, fastThreshold=9, scaleFactor=1.2
        )
        norma, umbral = cv2.NORM_HAMMING, 0.74
    elif metodo == "SIFT":
        detector = cv2.SIFT_create(nfeatures=6500)
        norma, umbral = cv2.NORM_L2, 0.72
    else:
        raise ValueError(f"Método de alineación no soportado: {metodo}")

    puntos_template, descriptores_template = detector.detectAndCompute(
        template, None
    )
    puntos_foto, descriptores_foto = detector.detectAndCompute(foto, None)
    if (
        descriptores_template is None
        or descriptores_foto is None
        or len(puntos_template) < 4
        or len(puntos_foto) < 4
    ):
        return None

    coincidencias_knn = cv2.BFMatcher(norma).knnMatch(
        descriptores_template, descriptores_foto, k=2
    )
    coincidencias = [
        primer
        for pareja in coincidencias_knn
        if len(pareja) == 2
        for primer, segundo in [pareja]
        if primer.distance < umbral * segundo.distance
    ]
    if len(coincidencias) < 40:
        return None

    origen = np.float32(
        [puntos_template[match.queryIdx].pt for match in coincidencias]
    )
    destino = np.float32(
        [puntos_foto[match.trainIdx].pt for match in coincidencias]
    )
    homografia, mascara = cv2.findHomography(
        origen,
        destino,
        cv2.RANSAC,
        4.0,
        maxIters=10000,
        confidence=0.998,
    )
    if homografia is None:
        return None
    return homografia, {"src": origen, "dst": destino}, mascara


# PASO 3.5 — Visualiza esquinas y marcadores detectados.
def _dibujar_deteccion(
    foto: Imagen,
    homografia: Imagen,
    evaluacion: Mapping[str, Any],
    datos: Mapping[str, Any],
) -> Imagen:
    """Marca el borde encontrado y los marcadores de la plantilla."""
    visualizacion = foto.copy()
    esquinas = np.round(
        np.array(evaluacion["esquinas_en_fotografia_px"])
    ).astype(np.int32)
    cv2.polylines(
        visualizacion, [esquinas.reshape(-1, 1, 2)], True, (0, 205, 0), 4
    )
    # VERDE = posición proyectada, NARANJA = centro negro observado.
    for nombre, punto in datos["marcadores_px"].items():
        estimado = cv2.perspectiveTransform(
            np.float32(punto).reshape(1, 1, 2), homografia
        )[0, 0]
        cv2.circle(visualizacion, tuple(np.round(estimado).astype(int)),
                   12, (0, 180, 0), 2)
    observados = evaluacion.get("marcadores", {}).get("marcadores_foto_original_px", {})
    for nombre, punto in observados.items():
        cv2.circle(visualizacion, tuple(np.round(punto).astype(int)),
                   7, (0, 170, 255), 2)
    return visualizacion


# PASO 3.2 — Prueba ORB/SIFT y selecciona la geometría válida.
def _seleccionar_homografia(
    plantilla: Imagen, foto: Imagen, metodo: str
) -> tuple[Imagen, Diccionario] | None:
    """Selecciona la geometría mejor cubierta entre ORB y SIFT."""
    alto, ancho = plantilla.shape
    alto_foto, ancho_foto = foto.shape
    metodos = ("ORB", "SIFT") if metodo == "AUTO" else (metodo,)
    candidatos = []

    for metodo_actual in metodos:
        coincidencias = extraer_coincidencias(
            plantilla, foto, metodo_actual
        )
        if coincidencias is None:
            print(f"{metodo_actual}: sin suficientes coincidencias")
            continue

        homografia, puntos, mascara = coincidencias
        evaluacion = medidas_homografia(
            homografia,
            puntos["src"],
            puntos,
            mascara,
            ancho,
            alto,
            ancho_foto,
            alto_foto,
        )
        if evaluacion is None:
            print(
                f"{metodo_actual}: geometría o cobertura de coincidencias rechazada"
            )
            continue

        evaluacion["metodo"] = metodo_actual
        puntuacion = (
            evaluacion["inliers"]
            * evaluacion["cobertura_convexa_plantilla"]
        )
        candidatos.append((puntuacion, homografia, evaluacion))

    if not candidatos:
        return None
    _, homografia, evaluacion = max(candidatos, key=lambda item: item[0])
    return homografia, evaluacion


# PASO 3.1 — Alinea una fotografía y guarda diagnóstico geométrico; si se solicita.
def alinear(
    foto_path: str | Path,
    carpeta: str | Path,
    metodo: str = "AUTO",
    prefijo: str = "cartilla",
    alineacion_local: bool = False,
) -> Diccionario:
    """Alinea la foto y guarda la imagen, visualización y reporte geométrico."""
    carpeta = Path(carpeta)
    foto_path = Path(foto_path)
    datos = json.loads(
        _ruta_coordenadas(carpeta).read_text(encoding="utf-8")
    )
    ruta_plantilla = carpeta / "02_3_plantilla_maestra_sin_marcas.png"
    if not ruta_plantilla.exists():
        ruta_plantilla = carpeta / "plantilla_maestra.png"
    plantilla = _leer_imagen(ruta_plantilla, cv2.IMREAD_COLOR)
    foto = _leer_imagen(foto_path, cv2.IMREAD_COLOR)
    plantilla_gris = cv2.cvtColor(plantilla, cv2.COLOR_BGR2GRAY)
    foto_gris = cv2.cvtColor(foto, cv2.COLOR_BGR2GRAY)

    # PASO 3.10 — No obligar cuatro cuadrados: comparar ORB, SIFT y
    # correcciones opcionales, conservando el mejor registro interior.
    alto, ancho = plantilla_gris.shape
    alto_foto, ancho_foto = foto_gris.shape
    metodos = ("ORB", "SIFT") if metodo == "AUTO" else (metodo,)
    intentos = []
    validos = []
    ruta_reporte = carpeta / f"{prefijo}_reporte.json"

    for metodo_actual in metodos:
        matches = extraer_coincidencias(plantilla_gris, foto_gris, metodo_actual)
        if matches is None:
            intentos.append({"metodo": metodo_actual, "motivo": "Sin coincidencias suficientes"})
            continue
        h_inicial, puntos, inliers = matches
        geometria = medidas_homografia(
            h_inicial, puntos["src"], puntos, inliers,
            ancho, alto, ancho_foto, alto_foto,
        )
        if geometria is None:
            intentos.append({"metodo": metodo_actual, "motivo": "Geometría ORB/SIFT inválida"})
            continue
        geometria["metodo"] = metodo_actual
        ajuste, info_marcadores = refinar_con_marcadores(
            foto_gris, plantilla_gris, h_inicial,
            datos.get("marcadores_px", {}),
        )
        opciones = [("sin_refinamiento", h_inicial)]
        if ajuste is not None:
            opciones.append((info_marcadores["metodo_correccion"], ajuste))
        # Si una detección de cuatro cuadrados incluye un falso positivo,
        # contrastar correcciones excluyendo una esquina a la vez.
        opciones.extend(hipotesis_tres_de_cuatro(h_inicial, info_marcadores, ancho, alto))
        intentos_metodo = []
        # El ECC solo debe aplicarse a la mejor hipótesis inicialmente
        # rechazada de cada detector. Evita ajustar sobre múltiples variantes
        # y mantiene el coste acotado en fotos difíciles.
        mejor_fallida = None
        for nombre_hipotesis, homografia_candidata in opciones:
            try:
                corregida_candidata = cv2.warpPerspective(
                    foto_gris, np.linalg.inv(homografia_candidata),
                    (ancho, alto), flags=cv2.INTER_LINEAR,
                    borderMode=cv2.BORDER_CONSTANT, borderValue=255,
                )
            except (cv2.error, np.linalg.LinAlgError):
                continue
            cuadricula = verificar_cuadricula(corregida_candidata, plantilla_gris, datos)
            muestras = cuadricula.get("muestras", [])
            # Desempate: menor error local y mayor similitud de cuadrícula.
            puntaje = (np.mean([x["error_px"] for x in muestras])
                       + .35*max([x["error_px"] for x in muestras])
                       - .9*np.mean([x["correlacion"] for x in muestras])) if muestras else 1e6
            intento = {"hipotesis": nombre_hipotesis,
                       "cuadricula_valida": bool(cuadricula["valido"]),
                       "error_maximo_px": cuadricula.get("error_maximo_local_px"),
                       "correlacion_minima": cuadricula.get("correlacion_minima"),
                       "puntaje": round(float(puntaje), 3)}
            intentos_metodo.append(intento)
            if cuadricula["valido"]:
                validos.append((puntaje, nombre_hipotesis, homografia_candidata,
                                geometria, cuadricula, info_marcadores, None, None))
            elif (muestras and cuadricula.get("correlacion_minima", 0) >= 0.27
                  and cuadricula.get("error_maximo_local_px", 1e9) <= 12.0):
                if mejor_fallida is None or puntaje < mejor_fallida[0]:
                    mejor_fallida = (puntaje, nombre_hipotesis, homografia_candidata,
                                    corregida_candidata)
        # Segunda oportunidad SOLO cuando ninguna hipótesis del detector validó.
        # La aceptación depende, otra vez, de la misma verificación estricta.
        if (not any(item[3]["metodo"] == metodo_actual for item in validos)
                and mejor_fallida is not None):
            puntaje_prev, nombre_prev, homografia_prev, imagen_prev = mejor_fallida
            corregida_ecc, informe_ecc = mejora_ecc(imagen_prev, plantilla_gris, datos)
            intento_ecc = {"hipotesis": f"{nombre_prev}+ECC",
                           "ecc": informe_ecc, "cuadricula_valida": False}
            if informe_ecc.get("aplicado", False):
                cuadro_ecc = verificar_cuadricula(corregida_ecc, plantilla_gris, datos)
                intento_ecc["cuadricula_valida"] = bool(cuadro_ecc["valido"])
                intento_ecc["error_maximo_px"] = cuadro_ecc.get("error_maximo_local_px")
                intento_ecc["correlacion_minima"] = cuadro_ecc.get("correlacion_minima")
                if cuadro_ecc["valido"]:
                    muestras_ecc = cuadro_ecc["muestras"]
                    puntaje_ecc = (np.mean([x["error_px"] for x in muestras_ecc])
                                  + .35 * max(x["error_px"] for x in muestras_ecc)
                                  - .9 * np.mean([x["correlacion"] for x in muestras_ecc]))
                    validos.append((puntaje_ecc, f"{nombre_prev}+ECC",
                                    homografia_prev, geometria, cuadro_ecc,
                                    info_marcadores, informe_ecc, None))
            intentos_metodo.append(intento_ecc)
        # Tercera oportunidad EXPERIMENTAL y opt-in: alinear la zona de
        # respuestas con un desplazamiento suave, con 24 zonas de validación
        # distintas de las usadas para ajustar la deformación.
        if (alineacion_local and
                not any(item[3]["metodo"] == metodo_actual for item in validos)
                and mejor_fallida is not None):
            _, nombre_prev, homografia_prev, imagen_prev = mejor_fallida
            mapa, info_local = corregir_cuadricula_local(
                imagen_prev, plantilla_gris, datos
            )
            intentos_metodo.append({"hipotesis": f"{nombre_prev}+LOCAL",
                                   "alineacion_local": info_local})
            if mapa is not None:
                cuadricula_local = info_local["cuadricula"]
                muestras = cuadricula_local["muestras"]
                puntuacion_local = (np.mean([x["error_px"] for x in muestras])
                                   + .35 * max(x["error_px"] for x in muestras)
                                   - .9 * np.mean([x["correlacion"] for x in muestras]))
                validos.append((puntuacion_local, f"{nombre_prev}+LOCAL",
                                homografia_prev, geometria, cuadricula_local,
                                info_marcadores, None, (mapa, info_local)))
        intentos.append({"metodo": metodo_actual,
                         "marcadores_detectados": info_marcadores.get("marcadores_detectados", 0),
                         "hipotesis": intentos_metodo})

    if not validos:
        reporte = {
            "valido": False,
            "motivo": "Ninguna hipótesis ORB/SIFT, con o sin marcadores, validó la cuadrícula interior",
            "intentos": intentos,
        }
        guardar_json(ruta_reporte, reporte)
        print("RECHAZADA:", reporte["motivo"])
        return reporte
    _, nombre_hipotesis, homografia, evaluacion, cuadricula, marcadores, ecc_aplicado, ajuste_local = min(
        validos, key=lambda item: item[0]
    )
    evaluacion = dict(evaluacion)
    evaluacion["cuadricula"] = cuadricula
    evaluacion["marcadores"] = marcadores
    evaluacion["hipotesis_seleccionada"] = nombre_hipotesis
    evaluacion["ecc_automatico"] = ecc_aplicado
    evaluacion["alineacion_local"] = ajuste_local[1] if ajuste_local else None
    evaluacion["intentos"] = intentos
    metodos_validos = {i[3]["metodo"] for i in validos}
    cuadrados = marcadores.get("marcadores_detectados", 0)
    evaluacion["metodos_alternativos_validos"] = sorted(metodos_validos)
    # Si sólo una familia o pocos marcadores verifican la geometría,
    # permitir lectura diagnosticada pero impedir calificación sin revisión.
    evaluacion["revision_geometrica_recomendada"] = (
        len(metodos_validos) < 2 or cuadrados < 3 or ajuste_local is not None
    )
    corregida = cv2.warpPerspective(
        foto, np.linalg.inv(homografia),
        (ancho, alto), flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255),
    )
    if ajuste_local is not None:
        mapa_x, mapa_y = ajuste_local[0]
        corregida = cv2.remap(
            corregida, mapa_x, mapa_y, interpolation=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255),
        )
    if ecc_aplicado is not None and ecc_aplicado.get("aplicado", False):
        corregida = cv2.warpAffine(
            corregida, np.asarray(ecc_aplicado["matriz"], dtype=np.float32),
            (ancho, alto), flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP,
            borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255),
        )

    nombre_alineada = f"{prefijo}_alineada.png"
    ruta_alineada = carpeta / nombre_alineada
    if not cv2.imwrite(str(ruta_alineada), corregida):
        raise OSError(f"No se pudo guardar la imagen: {ruta_alineada}")

    visualizacion = _dibujar_deteccion(
        foto, homografia, evaluacion, datos
    )
    ruta_deteccion = carpeta / f"{prefijo}_deteccion.jpg"
    if not cv2.imwrite(
        str(ruta_deteccion),
        visualizacion,
        [cv2.IMWRITE_JPEG_QUALITY, 92],
    ):
        raise OSError(f"No se pudo guardar la imagen: {ruta_deteccion}")

    reporte = {
        "valido": True,
        "imagen_fuente": foto_path.name,
        "imagen_resultado": nombre_alineada,
        "metricas": evaluacion,
        "revision_geometrica_recomendada": evaluacion["revision_geometrica_recomendada"],
        "nota": (
            "Validacion geometrica preliminar; no es garantia "
            "de lectura correcta."
        ),
    }
    guardar_json(ruta_reporte, reporte)
    print("ALINEACION ACEPTADA:", evaluacion["metodo"])
    print(
        "Inliers:",
        evaluacion["inliers"],
        "/ coincidencias:",
        evaluacion["coincidencias_iniciales"],
    )
    print("Cobertura de inliers:", evaluacion["cobertura_convexa_plantilla"])
    print("Error mediano:", evaluacion["error_mediano_px"], "px")
    print("Imagen corregida:", ruta_alineada.resolve())
    return reporte

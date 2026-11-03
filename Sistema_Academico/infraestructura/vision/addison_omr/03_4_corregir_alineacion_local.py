"""PASO 3.8 bis — rescate EXPERIMENTAL con deformación local suave.

Sólo se usa si fallan ORB/SIFT, esquinas y ECC; necesita solicitud
expresa (--alineacion-local). No declara una hoja apta para calificar:
siempre exige revisión humana, incluso cuando valide la cuadrícula.
"""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any
import cv2
import numpy as np
from .definir_parametros_omr import Imagen
from .validar_cuadricula_respuestas import verificar_cuadricula

_ANCLAS = (1, 8, 13, 20, 27, 29)  # índices locales, excluyen 5/15/25 del validador
_CONTROLES = (4, 11, 17, 24, 26)  # segunda familia de puntos no usados en el ajuste


def _correspondencia(
    referencia: Imagen, foto: Imagen, datos: Mapping[str, Any],
    columna: int, fila: int, margen: int = 15,
) -> tuple[float, float, float, float, float]:
    """(x, y, desplazamiento x/y, correlación) en cuadrícula impresa."""
    pregunta = datos["respuestas"][columna * 30 + fila]
    burbujas = list(pregunta["opciones"].values())
    x = int(round(np.mean([b["centro_px"][0] for b in burbujas])))
    y = int(round(np.mean([b["centro_px"][1] for b in burbujas])))
    sx, sy = 50, 42
    x0, x1 = x - sx // 2, x + sx // 2
    y0, y1 = y - sy // 2, y + sy // 2
    if (x0 - margen < 0 or y0 - margen < 0 or
            x1 + margen > foto.shape[1] or y1 + margen > foto.shape[0]):
        raise ValueError("Ancla local fuera de imagen")
    patron = referencia[y0:y1, x0:x1]
    region = foto[y0-margen:y1+margen, x0-margen:x1+margen]
    similitud = cv2.matchTemplate(region, patron, cv2.TM_CCOEFF_NORMED)
    _, puntuacion, _, (dx, dy) = cv2.minMaxLoc(similitud)
    return float(x), float(y), float(dx-margen), float(dy-margen), float(puntuacion)


def corregir_cuadricula_local(
    imagen: Imagen, referencia: Imagen, datos: Mapping[str, Any]
) -> tuple[tuple[Imagen, Imagen] | None, dict[str, Any]]:
    """Obtiene remapeo 2D desde 18 anclas y valida zonas INDEPENDIENTES.

    El mapa se desvanece hasta cero antes del encabezado (DNI y área): la deformación modelada
    sólo es fiable cerca de las columnas de preguntas. El resultado debe ser
    comprobado otra vez por la verificación geométrica original.
    """
    diagnostico: dict[str, Any] = {"aplicado": False, "experimental": True}
    try:
        foto = cv2.GaussianBlur(imagen, (3, 3), 0)
        patron = cv2.GaussianBlur(referencia, (3, 3), 0)
        columnas = [[_correspondencia(patron, foto, datos, c, j)
                     for j in _ANCLAS] for c in range(3)]
    except (ValueError, cv2.error) as error:
        diagnostico["motivo"] = str(error)
        return None, diagnostico
    confianzas = [p[4] for col in columnas for p in col]
    if min(confianzas) < 0.35:
        diagnostico["motivo"] = "Anclas locales con poca semejanza de impresión"
        diagnostico["correlacion_minima_anclas"] = round(float(min(confianzas)), 3)
        return None, diagnostico
    cxs = np.asarray([col[0][0] for col in columnas], dtype=np.float64)
    cys = np.asarray([p[1] for p in columnas[0]], dtype=np.float64)
    dxs = np.asarray([[p[2] for p in col] for col in columnas])
    dys = np.asarray([[p[3] for p in col] for col in columnas])
    magnitudes = np.hypot(dxs, dys)
    if np.max(magnitudes) > 14 or np.max(np.abs(np.diff(dxs, axis=1))) > 13 or np.max(np.abs(np.diff(dys, axis=1))) > 13:
        diagnostico["motivo"] = "Correcciones locales demasiado grandes o irregulares"
        return None, diagnostico
    alto, ancho = imagen.shape
    xx = np.arange(ancho, dtype=np.float32)
    yy = np.arange(alto, dtype=np.float32)
    desplazamientos_x = np.stack([np.interp(yy, cys, v) for v in dxs], axis=1)
    desplazamientos_y = np.stack([np.interp(yy, cys, v) for v in dys], axis=1)
    posiciones = np.clip(xx, float(cxs[0]), float(cxs[-1]))
    k = np.clip(np.searchsorted(cxs, posiciones, side="right") - 1, 0, 1)
    t = (posiciones - cxs[k]) / (cxs[k + 1] - cxs[k])
    # Fundir a desplazamiento cero 150 px antes de la primera columna de
    # preguntas, evitando mover DNI/área que no se calibran aquí.
    peso_izquierda = np.clip((xx - (cxs[0] - 160)) / 160, 0, 1)
    mapa_x = np.empty((alto, ancho), dtype=np.float32)
    mapa_y = np.empty((alto, ancho), dtype=np.float32)
    for j in range(ancho):
        n, f = int(k[j]), float(t[j])
        a = desplazamientos_x[:, n] * (1-f) + desplazamientos_x[:, n+1] * f
        b = desplazamientos_y[:, n] * (1-f) + desplazamientos_y[:, n+1] * f
        mapa_x[:, j] = j + a * peso_izquierda[j]
        mapa_y[:, j] = yy + b * peso_izquierda[j]
    corregida = cv2.remap(imagen, mapa_x, mapa_y, interpolation=cv2.INTER_LINEAR,
                          borderMode=cv2.BORDER_CONSTANT, borderValue=255)
    validacion = verificar_cuadricula(corregida, referencia, datos)
    diagnostico.update({"correlacion_minima_anclas": round(float(min(confianzas)), 3),
                        "maximo_desplazamiento_px": round(float(magnitudes.max()), 2),
                        "cuadricula": validacion})
    if not validacion.get("valido"):
        diagnostico["motivo"] = "No pasó las nueve zonas de cuadrícula independientes"
        return None, diagnostico
    # Segundo control independiente, en otras 15 preguntas no calibradas.
    foto_corregida = cv2.GaussianBlur(corregida, (3, 3), 0)
    fallos = []
    muestras = []
    tolerancia = validacion["tolerancia_local_px"]
    for c in range(3):
        for fila in _CONTROLES:
            x, y, dx, dy, corr = _correspondencia(patron, foto_corregida, datos, c, fila, margen=8)
            muestras.append({"pregunta": c*30+fila+1, "desplazamiento_px": round(float(np.hypot(dx,dy)), 2),
                             "correlacion": round(corr,3)})
            if corr < .27 or np.hypot(dx, dy) > tolerancia:
                fallos.append(c*30+fila+1)
    diagnostico["verificacion_adicional"] = {"muestras": muestras, "fallos": fallos}
    if fallos:
        diagnostico["motivo"] = "Fallaron controles independientes adicionales"
        return None, diagnostico
    diagnostico["aplicado"] = True
    diagnostico["motivo"] = "Cuadrícula validada en 24 regiones no utilizadas para estimar la deformación; requiere revisión humana"
    return (mapa_x, mapa_y), diagnostico

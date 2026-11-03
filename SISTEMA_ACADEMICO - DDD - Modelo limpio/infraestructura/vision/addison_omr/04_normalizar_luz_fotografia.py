"""Normalización de iluminación y diagnóstico de calidad de imagen."""

# ===================================================================
# MAPA DE REVISIÓN: pasos 4.1, 4.2, 9.4
# Consulta 00_LEER_SECUENCIA.md para recorrer el algoritmo en orden.
# La numeración es documental; no cambia llamadas ni nombres Python.
# ===================================================================


from __future__ import annotations

import cv2
import numpy as np
from .definir_parametros_omr import Diccionario, Imagen, UMBRAL_FOCO


# PASO 4.2 — Compensa diferencias de iluminación local.
def normalizar_luz(gris: Imagen, metodo: str = "suave") -> Imagen:
    """Compensa las variaciones de iluminación en la fotografía."""
    fondo = cv2.GaussianBlur(gris, (0, 0), sigmaX=45, sigmaY=45)
    escala = 220 if metodo == "suave" else 255
    imagen = cv2.divide(gris, np.maximum(fondo, 1), scale=escala)
    if metodo == "contraste":
        imagen = cv2.createCLAHE(
            clipLimit=2.0, tileGridSize=(8, 8)
        ).apply(imagen)
    return imagen


# PASO 4.1 — Crea variantes suave, contraste y respaldo.
def tratamientos(gris: Imagen) -> dict[str, Imagen]:
    """Crea tres procesamientos correlacionados de la misma fotografía."""
    suave = normalizar_luz(gris, "suave")
    contraste = normalizar_luz(gris, "contraste")

    fondo = cv2.GaussianBlur(gris, (0, 0), sigmaX=45, sigmaY=45)
    base = cv2.divide(gris, np.maximum(fondo, 1), scale=235)
    respaldo = cv2.createCLAHE(
        clipLimit=1.5, tileGridSize=(8, 8)
    ).apply(base)
    return {"suave": suave, "contraste": contraste, "respaldo": respaldo}


# PASO 9.4 — Evalúa nitidez y distribución luminosa de la fotografía.
def evaluar_calidad(gris: Imagen) -> Diccionario:
    """Mide la calidad aparente: NO estima probabilidad de lectura correcta."""
    mitad = cv2.resize(
        gris, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA
    )
    foco = float(cv2.Laplacian(mitad, cv2.CV_32F).var())
    percentil_5, percentil_50, percentil_95 = map(
        float, np.percentile(mitad, [5, 50, 95])
    )
    luz_lenta = cv2.GaussianBlur(mitad, (0, 0), sigmaX=25, sigmaY=25)
    luz_10, luz_90 = np.percentile(luz_lenta, [10, 90])
    desigualdad = float(luz_90 - luz_10)

    advertencias = []
    if foco < UMBRAL_FOCO:
        advertencias.append("Nitidez aparente baja; revisar visualmente")
    if percentil_95 - percentil_5 < 60:
        advertencias.append("Rango tonal reducido")
    if desigualdad > 55:
        advertencias.append("Iluminacion muy desigual")

    return {
        "varianza_laplaciano_mitad": round(foco, 2),
        "gris_percentiles_5_50_95": [
            round(percentil_5, 2),
            round(percentil_50, 2),
            round(percentil_95, 2),
        ],
        "rango_tonal_p95_p5": round(percentil_95 - percentil_5, 2),
        "desigualdad_luminosa_p90_p10": round(desigualdad, 2),
        "advertencias": advertencias,
    }

"""Extracción de medidas de oscuridad y contraste para cada burbuja."""

# ===================================================================
# MAPA DE REVISIÓN: pasos 5.1, 5.2
# Consulta 00_LEER_SECUENCIA.md para recorrer el algoritmo en orden.
# La numeración es documental; no cambia llamadas ni nombres Python.
# ===================================================================


from __future__ import annotations

from collections.abc import Mapping
import numpy as np
from .definir_parametros_omr import Burbuja, Diccionario, Imagen


# PASO 5.1 — Aplica la medición sobre un grupo de opciones.
def _medir_burbujas(
    imagen: Imagen, burbujas: Mapping[str, Burbuja]
) -> dict[str, Diccionario]:
    return {
        opcion: medir_circulo(imagen, burbuja)
        for opcion, burbuja in burbujas.items()
    }


# PASO 5.2 — Extrae fracción oscura, contraste y fondo por burbuja.
def medir_circulo(gris: Imagen, burbuja: Burbuja) -> Diccionario:
    """Calcula oscuridad y contraste en el centro de una burbuja.

    El centro evita el borde impreso; la corona estima la iluminación local.
    Los caracteres impresos se descontarán en etapas posteriores.
    """
    centro_x, centro_y = map(float, burbuja["centro_px"])
    radio = float(burbuja["radio_px"])
    margen = int(np.ceil(radio * 1.5)) + 2

    x0 = max(0, int(centro_x) - margen)
    y0 = max(0, int(centro_y) - margen)
    x1 = min(gris.shape[1], int(centro_x) + margen + 2)
    y1 = min(gris.shape[0], int(centro_y) + margen + 2)
    region = gris[y0:y1, x0:x1]

    if region.size == 0:
        raise ValueError(f"Burbuja fuera de imagen: {centro_x}, {centro_y}")

    posiciones_y, posiciones_x = np.ogrid[y0:y1, x0:x1]
    distancias = np.hypot(posiciones_x - centro_x, posiciones_y - centro_y)
    interior = region[distancias < radio * 0.59].astype(np.float32)
    corona = region[
        (distancias > radio * 1.12) & (distancias < radio * 1.42)
    ].astype(np.float32)

    if interior.size < 30 or corona.size < 15:
        raise ValueError(
            f"Muestras insuficientes para burbuja en {centro_x}, {centro_y}"
        )

    fondo_local = float(np.percentile(corona, 72))
    fraccion_oscura = float(np.mean(interior < fondo_local - 65.0))
    contraste_local = float(fondo_local - np.mean(interior))
    return {
        "fraccion_oscura": round(fraccion_oscura, 5),
        "contraste_local": round(contraste_local, 2),
        "fondo_local": round(fondo_local, 1),
    }

"""Constantes, umbrales experimentales y tipos compartidos."""

# PASO 0 — Parámetros compartidos por las etapas 1–10.
# No se ejecuta como fase autónoma: define constantes y tipos.

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import numpy as np

VERSION = "0.5.4-experimental"
TOTAL_PREGUNTAS = 90
TOTAL_COLUMNAS_DNI = 8
SECCIONES_CONTROL = ("turno", "area", "tema")
ESTADOS = ("VALIDA", "SIN_RESPUESTA", "DUDOSA", "DOBLE_MARCA")

# Los umbrales proceden del prototipo original. NO están calibrados con una
# muestra etiquetada y no deben modificarse sin pruebas de regresión.
UMBRAL_FOCO = 150.0
UMBRAL_ERROR_ALINEACION = 2.3
ESCALA_ECC = 0.5

# Colores BGR de OpenCV, no RGB.
COLORES_ESTADO = {
    "VALIDA": (34, 150, 40),
    "DUDOSA": (0, 170, 255),
    "DOBLE_MARCA": (35, 35, 235),
    "SIN_RESPUESTA": (165, 165, 165),
}
COLOR_REVISION = (0, 165, 255)

Diccionario = dict[str, Any]
Burbuja = Mapping[str, Any]
Imagen = np.ndarray

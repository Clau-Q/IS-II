"""Utilidades para recorrer las burbujas y encontrar sus coordenadas."""

# ===================================================================
# MAPA DE REVISIÓN: pasos 2.3, 2.4
# Consulta 00_LEER_SECUENCIA.md para recorrer el algoritmo en orden.
# La numeración es documental; no cambia llamadas ni nombres Python.
# ===================================================================


from __future__ import annotations

from typing import Any
from collections.abc import Iterator
from collections.abc import Mapping
from .definir_parametros_omr import Burbuja, SECCIONES_CONTROL


# PASO 2.3 — Itera burbujas en respuestas, DNI y encabezado.
def _iterar_burbujas(datos: Mapping[str, Any]) -> Iterator[Burbuja]:
    """Recorre las burbujas de respuestas, DNI y encabezado."""
    for pregunta in datos["respuestas"]:
        yield from pregunta["opciones"].values()

    for columna in datos["dni"]:
        yield from columna["digitos"].values()

    for seccion in SECCIONES_CONTROL:
        yield from datos[seccion].values()


# PASO 2.4 — Obtiene el centro de una burbuja en píxeles.
def _centro(burbuja: Burbuja) -> tuple[int, int]:
    return tuple(round(valor) for valor in burbuja["centro_px"])

"""Persistencia de JSON, CSV e imagen de revisión."""

# ===================================================================
# MAPA DE REVISIÓN: pasos 10.1, 10.5
# Consulta 00_LEER_SECUENCIA.md para recorrer el algoritmo en orden.
# La numeración es documental; no cambia llamadas ni nombres Python.
# ===================================================================


from __future__ import annotations

from typing import Any
from collections.abc import Mapping
from pathlib import Path
from collections.abc import Sequence
import csv
import cv2
from .definir_parametros_omr import Imagen
from .cargar_plantilla_referencia import guardar_json


# PASO 10.5 — Exporta decisiones por pregunta a CSV.
def _guardar_csv(ruta: Path, respuestas: Sequence[Mapping[str, Any]]) -> None:
    columnas = [
        "pregunta",
        "respuesta",
        "estado",
        "confianza",
        "candidatas",
        "requiere_revision_manual",
        "origen",
        "coincidencia_metodos",
    ]
    with ruta.open("w", newline="", encoding="utf-8-sig") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(columnas)
        for respuesta in respuestas:
            escritor.writerow(
                [
                    respuesta["pregunta"],
                    respuesta["respuesta"] or "",
                    respuesta["estado"],
                    respuesta["confianza"],
                    "/".join(respuesta["candidatas"]),
                    respuesta.get("requiere_revision_manual", False),
                    respuesta["fuente_evidencia"],
                    respuesta["coincidencia_metodos"],
                ]
            )


# PASO 10.1 — Guarda los resultados y solicita anotación y CSV.
def _guardar_resultados(
    prefijo: Path,
    gris: Imagen,
    datos: Mapping[str, Any],
    resultado: Mapping[str, Any],
) -> None:
    """Escribe JSON, CSV y JPG de revisión usando el prefijo indicado."""
    prefijo.parent.mkdir(parents=True, exist_ok=True)
    guardar_json(Path(f"{prefijo}.json"), resultado)
    _guardar_csv(Path(f"{prefijo}.csv"), resultado["respuestas"])

    # Generación de imagen únicamente para diagnóstico visual: es prescindible.
    try:
        from .debug_dibujar_imagen_revision import anotacion
    except ModuleNotFoundError as error:
        if error.name != __package__ + ".debug_dibujar_imagen_revision":
            raise
        return  # JSON y CSV ya se guardaron.

    visualizacion = anotacion(gris, datos, resultado)
    ruta_visualizacion = Path(f"{prefijo}_revision.jpg")
    if not cv2.imwrite(
        str(ruta_visualizacion),
        visualizacion,
        [cv2.IMWRITE_JPEG_QUALITY, 92],
    ):
        raise OSError(f"No se pudo guardar la imagen: {ruta_visualizacion}")

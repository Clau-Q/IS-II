"""Carga de imágenes, validación de plantilla y persistencia JSON."""

# ===================================================================
# MAPA DE REVISIÓN: pasos 2.1, 2.2, 10.6
# Consulta 00_LEER_SECUENCIA.md para recorrer el algoritmo en orden.
# La numeración es documental; no cambia llamadas ni nombres Python.
# ===================================================================


from __future__ import annotations

from typing import Any
from collections.abc import Mapping
from pathlib import Path
import cv2
import json
from .definir_parametros_omr import Diccionario, Imagen, TOTAL_COLUMNAS_DNI, TOTAL_PREGUNTAS


# PASO 2.2 — Carga una imagen y verifica que exista.
def _leer_imagen(ruta: Path, modo: int) -> Imagen:
    """Abre una imagen y comunica claramente si no se pudo leer."""
    imagen = cv2.imread(str(ruta), modo)
    if imagen is None:
        raise FileNotFoundError(f"No se pudo abrir la imagen: {ruta}")
    return imagen


# Localiza el JSON numerado. Mantiene compatibilidad con las plantillas previas.
def _ruta_coordenadas(base: Path) -> Path:
    for nombre in ("02_2_mapa_coordenadas_burbujas.json", "plantilla_coordenadas.json"):
        ruta = base / nombre
        if ruta.is_file():
            return ruta
    raise FileNotFoundError(
        f"Falta el JSON de coordenadas en {base}: "
        "02_2_mapa_coordenadas_burbujas.json o plantilla_coordenadas.json"
    )


# PASO 2.1 — Lee y valida la plantilla y el JSON de coordenadas.
def leer_datos(carpeta: str | Path) -> tuple[Diccionario, Imagen]:
    """Carga y valida la plantilla y su archivo de coordenadas."""
    base = Path(carpeta)
    ruta_coordenadas = _ruta_coordenadas(base)
    with ruta_coordenadas.open(encoding="utf-8") as archivo:
        datos = json.load(archivo)

    ruta_plantilla = (base / "02_3_plantilla_maestra_sin_marcas.png")
    if not ruta_plantilla.exists():
        ruta_plantilla = base / "plantilla_maestra.png"
    referencia = _leer_imagen(ruta_plantilla, cv2.IMREAD_GRAYSCALE)
    ancho_esperado = datos["ancho_px"]
    alto_esperado = datos["alto_px"]
    if referencia.shape[::-1] != (ancho_esperado, alto_esperado):
        raise ValueError(
            "La imagen de la plantilla no coincide con sus coordenadas."
        )

    if (
        len(datos["respuestas"]) != TOTAL_PREGUNTAS
        or len(datos["dni"]) != TOTAL_COLUMNAS_DNI
    ):
        raise ValueError("La plantilla debe contener 90 preguntas y 8 columnas DNI.")

    return datos, referencia


# PASO 10.6 — Escribe un JSON legible en UTF-8.
def guardar_json(ruta: str | Path, datos: Mapping[str, Any]) -> None:
    """Serializa un reporte UTF-8 con indentación legible."""
    Path(ruta).write_text(
        json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8"
    )

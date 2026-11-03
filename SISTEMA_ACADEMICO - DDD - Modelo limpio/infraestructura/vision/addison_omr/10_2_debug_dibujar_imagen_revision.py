"""Marcado de las burbujas y anotaciones para revisión visual."""

# ===================================================================
# MAPA DE REVISIÓN: pasos 10.2, 10.3, 10.4
# Consulta 00_LEER_SECUENCIA.md para recorrer el algoritmo en orden.
# La numeración es documental; no cambia llamadas ni nombres Python.
# ===================================================================


from __future__ import annotations

from typing import Any
from collections.abc import Mapping
import cv2
from .definir_parametros_omr import Burbuja, COLORES_ESTADO, COLOR_REVISION, Imagen, SECCIONES_CONTROL
from .localizar_burbujas import _centro


# PASO 10.3 — Dibuja el contorno de una opción detectada.
def _dibujar_burbuja(
    imagen: Imagen, burbuja: Burbuja, color: tuple[int, int, int]
) -> None:
    cv2.circle(
        imagen,
        _centro(burbuja),
        round(burbuja["radio_px"] * 0.92),
        color,
        2,
    )


# PASO 10.4 — Añade las etiquetas de duda y revisión.
def _dibujar_etiqueta(
    imagen: Imagen,
    burbuja: Burbuja,
    etiqueta: str,
    color: tuple[int, int, int],
) -> None:
    x, y = _centro(burbuja)
    cv2.putText(
        imagen,
        etiqueta,
        (x + 11, y + 4),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.43,
        color,
        1,
        cv2.LINE_AA,
    )


# PASO 10.2 — Dibuja el resultado sobre la imagen en gris.
def anotacion(
    imagen: Imagen, datos: Mapping[str, Any], resultado: Mapping[str, Any]
) -> Imagen:
    """Genera una vista para auditar preguntas, DNI y controles."""
    visualizacion = cv2.cvtColor(imagen, cv2.COLOR_GRAY2BGR)

    for pregunta, respuesta in zip(datos["respuestas"], resultado["respuestas"]):
        if respuesta["estado"] == "SIN_RESPUESTA":
            continue

        color = (
            COLOR_REVISION
            if respuesta.get("requiere_revision_manual")
            else COLORES_ESTADO[respuesta["estado"]]
        )
        for opcion in respuesta["candidatas"]:
            _dibujar_burbuja(
                visualizacion, pregunta["opciones"][opcion], color
            )

        if respuesta["estado"] in ("DUDOSA", "DOBLE_MARCA"):
            burbuja = pregunta["opciones"][respuesta["mejor_alternativa"]]
            _dibujar_etiqueta(
                visualizacion,
                burbuja,
                "?",
                COLORES_ESTADO[respuesta["estado"]],
            )
        if respuesta.get("requiere_revision_manual") and respuesta.get("respuesta"):
            _dibujar_etiqueta(
                visualizacion,
                pregunta["opciones"][respuesta["respuesta"]],
                "T",
                COLOR_REVISION,
            )

    for columna, respuesta in zip(datos["dni"], resultado["detalle_dni"]):
        if respuesta["candidatas"]:
            burbuja = columna["digitos"][respuesta["candidatas"][0]]
            _dibujar_burbuja(
                visualizacion, burbuja, COLORES_ESTADO[respuesta["estado"]]
            )

    for seccion in SECCIONES_CONTROL:
        decision = resultado["controles"][seccion]
        for opcion in decision["candidatas"]:
            _dibujar_burbuja(
                visualizacion,
                datos[seccion][opcion],
                COLORES_ESTADO[decision["estado"]],
            )

    return visualizacion

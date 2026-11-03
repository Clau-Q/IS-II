"""Etapa 03.3: validación LOCAL de la cuadricula impresa antes del OMR."""
from __future__ import annotations
from collections.abc import Mapping
from typing import Any
import cv2
import numpy as np
from .definir_parametros_omr import Imagen


# ETAPA 03.3 — Compara regiones interiores en 9 lugares de las tres columnas.
def verificar_cuadricula(
    imagen_alineada: Imagen, plantilla: Imagen, datos: Mapping[str, Any]
) -> dict[str, Any]:
    """Valida desplazamiento residual de impresión con NCC localizada.

    Cada región contiene varias burbujas impresas y separadores. El detector
    busca su desplazamiento dentro de +/-0.8 radios; si observa errores que
    perjudican la lectura, deniega su uso aunque ORB/SIFT esté satisfecho.
    """
    preguntas = datos["respuestas"]
    if len(preguntas) != 90 or imagen_alineada.shape != plantilla.shape:
        return {"valido": False, "motivo": "No coinciden forma y 90 preguntas"}
    radios = [float(b["radio_px"]) for p in preguntas for b in p["opciones"].values()]
    radio = float(np.median(radios))
    lado_x = max(50, int(round(radio * 10)))
    lado_y = max(40, int(round(radio * 8)))
    busqueda = max(4, int(round(radio * .85)))
    tolerancia = max(2.5, radio * .38)
    referencia_suave = cv2.GaussianBlur(plantilla, (3, 3), 0)
    foto_suave = cv2.GaussianBlur(imagen_alineada, (3, 3), 0)
    muestras = []
    for inicio in (0, 30, 60):
        for indice in (inicio+5, inicio+15, inicio+25):
            pregunta = preguntas[indice]
            burbujas = list(pregunta["opciones"].values())
            x = int(round(float(np.mean([b["centro_px"][0] for b in burbujas]))))
            y = int(round(float(np.mean([b["centro_px"][1] for b in burbujas]))))
            x0, y0 = x-lado_x//2, y-lado_y//2
            if min(x0-busqueda, y0-busqueda) < 0 or (
                x0+lado_x+busqueda >= plantilla.shape[1]
                or y0+lado_y+busqueda >= plantilla.shape[0]
            ):
                return {"valido": False, "motivo": "Zona de cuadrícula fuera de imagen"}
            patron = referencia_suave[y0:y0+lado_y, x0:x0+lado_x]
            region = foto_suave[y0-busqueda:y0+lado_y+busqueda,
                                 x0-busqueda:x0+lado_x+busqueda]
            correlacion = cv2.matchTemplate(region, patron, cv2.TM_CCOEFF_NORMED)
            _, mejor, _, (xx, yy) = cv2.minMaxLoc(correlacion)
            dx, dy = xx-busqueda, yy-busqueda
            muestras.append({"pregunta_referencia": pregunta["pregunta"],
                             "correlacion": round(float(mejor), 3),
                             "dx_px": dx, "dy_px": dy,
                             "error_px": round(float(np.hypot(dx, dy)), 2)})
    baja = [z for z in muestras if z["correlacion"] < .27]
    desplazada = [z for z in muestras if z["error_px"] > tolerancia]
    valido = not baja and not desplazada
    return {
        "valido": valido, "radio_burbuja_px": round(radio, 2),
        "tolerancia_local_px": round(tolerancia, 2),
        "error_maximo_local_px": max(z["error_px"] for z in muestras),
        "correlacion_minima": min(z["correlacion"] for z in muestras),
        "muestras": muestras,
        "motivo": ("Cuadrícula interior suficientemente registrada" if valido else
                   f"Cuadrícula descentrada: {len(desplazada)} regiones desplazadas, "
                   f"{len(baja)} regiones sin semejanza suficiente"),
    }

"""Combinación conservadora de las lecturas de distintas variantes de imagen."""

# ===================================================================
# MAPA DE REVISIÓN: pasos 7.3, 7.4, 7.5
# Consulta 00_LEER_SECUENCIA.md para recorrer el algoritmo en orden.
# La numeración es documental; no cambia llamadas ni nombres Python.
# ===================================================================


from __future__ import annotations

from typing import Any
from collections.abc import Mapping
from .definir_parametros_omr import Diccionario


# PASO 7.5 — Reduce una lectura a estado, respuesta y candidatas.
def _resumen_lectura(lectura: Mapping[str, Any]) -> Diccionario:
    return {
        "estado": lectura["estado"],
        "respuesta": lectura["respuesta"],
        "candidatas": lectura["candidatas"],
    }


# PASO 7.4 — Resuelve acuerdos y discrepancias entre dos tratamientos.
def consenso_item(a: Mapping[str, Any], b: Mapping[str, Any]) -> Diccionario:
    """Conserva acuerdos; ante discrepancias exige revisión."""
    estado_a, estado_b = a["estado"], b["estado"]
    estados_iguales = estado_a == estado_b
    coinciden = (
        (estados_iguales and estado_a == "VALIDA" and a["respuesta"] == b["respuesta"])
        or (estados_iguales and estado_a == "SIN_RESPUESTA")
        or (
            estados_iguales
            and estado_a == "DOBLE_MARCA"
            and set(a["candidatas"]) == set(b["candidatas"])
        )
    )
    resultado = dict(a)
    resultado["coincidencia_metodos"] = coinciden
    if coinciden and estado_a == "VALIDA":
        resultado["confianza"] = (
            "alta"
            if a["confianza"] == b["confianza"] == "alta"
            else "media"
        )
    elif not coinciden:
        candidatas = list(
            dict.fromkeys(
                (a.get("candidatas") or []) + (b.get("candidatas") or [])
            )
        )
        if not candidatas:
            candidatas = list(
                dict.fromkeys([a["mejor_alternativa"], b["mejor_alternativa"]])
            )
        resultado.update(
            estado="DUDOSA",
            respuesta=None,
            candidatas=candidatas,
            confianza="baja",
        )

    # Estos campos históricos se sustituyen por 'validaciones' en v0.5.
    resultado["metodo_suave"] = _resumen_lectura(a)
    resultado["metodo_contraste"] = _resumen_lectura(b)
    return resultado


# PASO 7.3 — Une dos lecturas y añade una tercera diagnóstica.
def combinar_opciones(
    lect_a: Mapping[str, Any],
    lect_b: Mapping[str, Any],
    adicional: Mapping[str, Any] | None,
    variante_a: str,
    variante_b: str,
) -> Diccionario:
    """Combina dos variantes principales y registra una tercera diagnóstica."""
    resultado = consenso_item(lect_a, lect_b)
    resultado.pop("metodo_suave", None)
    resultado.pop("metodo_contraste", None)
    resultado["validaciones"] = {
        variante_a: _resumen_lectura(lect_a),
        variante_b: _resumen_lectura(lect_b),
    }
    if adicional is not None:
        resultado["validaciones"]["tercero"] = _resumen_lectura(adicional)

    if resultado["estado"] == "VALIDA":
        if variante_a != "suave":
            # Contraste y respaldo usan CLAHE; no son evidencia independiente.
            resultado["confianza"] = "media"
            resultado["fuente_evidencia"] = "respaldo_por_contraste_correlacionado"
        else:
            resultado["fuente_evidencia"] = "consenso_suave_y_contraste"
    elif resultado["estado"] == "DUDOSA":
        if adicional is not None and adicional["estado"] == "VALIDA":
            opcion = adicional["respuesta"]
            if opcion and opcion not in resultado["candidatas"]:
                resultado["candidatas"].append(opcion)
        resultado["fuente_evidencia"] = "metodos_discrepantes"
    elif resultado["estado"] == "DOBLE_MARCA":
        resultado["fuente_evidencia"] = "posible_doble_marca"
    else:
        resultado["fuente_evidencia"] = "sin_marca_consistente"
    return resultado

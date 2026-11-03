"""Calibración K-Means y lectura inicial de preguntas, DNI y controles."""

# ===================================================================
# MAPA DE REVISIÓN: pasos 6.1, 6.2, 6.3, 6.4, 6.5
# Consulta 00_LEER_SECUENCIA.md para recorrer el algoritmo en orden.
# La numeración es documental; no cambia llamadas ni nombres Python.
# ===================================================================


from __future__ import annotations

from typing import Any
from collections.abc import Mapping
from collections.abc import Sequence
import cv2
import numpy as np
from .definir_parametros_omr import Diccionario, ESTADOS, Imagen, SECCIONES_CONTROL, VERSION
from .medir_tinta_burbujas import _medir_burbujas


# PASO 6.2 — Obtiene calibración de oscuridad con K-Means.
def kmeans_umbral(valores: Sequence[float]) -> Diccionario:
    """Obtiene un umbral de oscuridad a partir de dos grupos K-Means.

    Si la hoja está vacía, K-Means puede inventar dos grupos: en ese caso
    se declara la calibración como no fiable.
    """
    muestras = np.asarray(valores, dtype=np.float32).reshape(-1, 1)
    cv2.setRNGSeed(2022)
    _, etiquetas, centros = cv2.kmeans(
        muestras,
        2,
        None,
        (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_MAX_ITER, 100, 0.0001),
        15,
        cv2.KMEANS_PP_CENTERS,
    )
    grupo_claro, grupo_oscuro = sorted(float(x) for x in centros.flatten())
    separacion = grupo_oscuro - grupo_claro
    grupos_fiables = separacion >= 0.24 and grupo_oscuro >= 0.73
    umbral = (
        float(np.clip((grupo_oscuro + grupo_claro) / 2, 0.65, 0.79))
        if grupos_fiables
        else 0.72
    )
    return {
        "grupo_claro": round(grupo_claro, 4),
        "grupo_oscuro": round(grupo_oscuro, 4),
        "separacion": round(separacion, 4),
        "dos_grupos_fiables": grupos_fiables,
        "umbral_marcado": round(umbral, 4),
        "numero_cluster_oscuro": int(np.argmax(centros.ravel())),
        "conteos_clusters": [
            int(n) for n in np.bincount(etiquetas.ravel(), minlength=2)
        ],
    }


# PASO 6.4 — Construye el registro de la decisión inicial.
def _crear_decision(
    estado: str,
    candidatas: list[str],
    confianza: str,
    mejor_alternativa: str,
    margen: float,
) -> Diccionario:
    return {
        "respuesta": candidatas[0] if estado == "VALIDA" else None,
        "estado": estado,
        "candidatas": candidatas,
        "confianza": confianza,
        "mejor_alternativa": mejor_alternativa,
        "margen": round(margen, 4),
    }


# PASO 6.3 — Decide marca única, doble, dudosa o vacía.
def resolver_opciones(
    scores: Mapping[str, Diccionario],
    estadistica: Mapping[str, Any],
    *,
    control: bool = False,
) -> Diccionario:
    """Clasifica una pregunta o columna DNI según oscuridad central.

    ``control`` se conserva por compatibilidad con la firma anterior.
    Las confianzas son categorías heurísticas, no probabilidades.
    """
    _ = control
    umbral = estadistica["umbral_marcado"]
    grupos_fiables = estadistica["dos_grupos_fiables"]
    ranking = sorted(
        (
            (opcion, float(medida["fraccion_oscura"]))
            for opcion, medida in scores.items()
        ),
        key=lambda par: par[1],
        reverse=True,
    )
    mejor_opcion, mayor = ranking[0]
    segundo = ranking[1][1] if len(ranking) > 1 else 0.0
    margen = mayor - segundo
    seleccionadas = (
        [opcion for opcion, valor in ranking if valor >= umbral]
        if grupos_fiables
        else []
    )

    if len(seleccionadas) > 1:
        return _crear_decision(
            "DOBLE_MARCA", seleccionadas, "baja", mejor_opcion, margen
        )
    if len(seleccionadas) == 1:
        confianza = (
            "alta"
            if mayor >= max(0.84, umbral + 0.13) and margen >= 0.19
            else "media"
        )
        return _crear_decision(
            "VALIDA", seleccionadas, confianza, mejor_opcion, margen
        )

    posible_marca_tenue = (
        (grupos_fiables and mayor >= 0.54 and margen >= 0.10)
        or (not grupos_fiables and mayor >= 0.56)
    )
    if posible_marca_tenue:
        return _crear_decision(
            "DUDOSA", [mejor_opcion], "baja", mejor_opcion, margen
        )

    confianza = "media" if grupos_fiables else "baja"
    return _crear_decision(
        "SIN_RESPUESTA", [], confianza, mejor_opcion, margen
    )


# PASO 6.5 — Interpreta encabezados comparados con la referencia.
def resolver_controles(
    metrics: Mapping[str, Diccionario],
    metricas_vacias: Mapping[str, Diccionario],
    estadistica: Mapping[str, Any],
) -> Diccionario:
    """Distingue tinta añadida de texto impreso en turno, área y tema."""
    _ = estadistica  # Compatibilidad con el contrato del lector anterior.
    diferencias = {
        opcion: medicion["fraccion_oscura"]
        - metricas_vacias[opcion]["fraccion_oscura"]
        for opcion, medicion in metrics.items()
    }
    ranking = sorted(diferencias.items(), key=lambda par: par[1], reverse=True)
    mejor_opcion, mayor = ranking[0]
    siguiente = ranking[1][1] if len(ranking) > 1 else 0.0
    margen = mayor - siguiente
    fuertes = [opcion for opcion, diferencia in ranking if diferencia >= 0.28]

    if len(fuertes) > 1:
        decision = _crear_decision(
            "DOBLE_MARCA", fuertes, "baja", mejor_opcion, margen
        )
    elif len(fuertes) == 1:
        confianza = "alta" if mayor >= 0.48 and margen >= 0.20 else "media"
        decision = _crear_decision(
            "VALIDA", fuertes, confianza, mejor_opcion, margen
        )
    elif mayor >= 0.17 and margen >= 0.10:
        decision = _crear_decision(
            "DUDOSA", [mejor_opcion], "baja", mejor_opcion, margen
        )
    else:
        decision = _crear_decision(
            "SIN_RESPUESTA", [], "media", mejor_opcion, margen
        )

    decision["diferencia_con_pdf_vacio"] = {
        opcion: round(valor, 4) for opcion, valor in diferencias.items()
    }
    return decision


# PASO 6.1 — Clasifica preguntas, DNI y controles de una variante.
def leer(gris: Imagen, datos: Mapping[str, Any], referencia: Imagen) -> Diccionario:
    """Obtiene una lectura inicial usando una sola variante de imagen."""
    preguntas_medidas = [
        (pregunta, _medir_burbujas(gris, pregunta["opciones"]))
        for pregunta in datos["respuestas"]
    ]
    # La calibración se ajusta SOLO con preguntas, nunca con DNI/encabezado.
    puntuaciones = [
        medida["fraccion_oscura"]
        for _, mediciones in preguntas_medidas
        for medida in mediciones.values()
    ]
    calibracion = kmeans_umbral(puntuaciones)

    respuestas = [
        {
            "pregunta": pregunta["pregunta"],
            **resolver_opciones(mediciones, calibracion),
            "mediciones": mediciones,
        }
        for pregunta, mediciones in preguntas_medidas
    ]
    dni = []
    for columna in datos["dni"]:
        mediciones = _medir_burbujas(gris, columna["digitos"])
        dni.append(
            {
                "columna": columna["columna"],
                **resolver_opciones(mediciones, calibracion),
                "mediciones": mediciones,
            }
        )

    controles = {}
    for seccion in SECCIONES_CONTROL:
        mediciones = _medir_burbujas(gris, datos[seccion])
        mediciones_vacias = _medir_burbujas(referencia, datos[seccion])
        controles[seccion] = {
            **resolver_controles(mediciones, mediciones_vacias, calibracion),
            "mediciones": mediciones,
        }

    conteos = {
        estado: sum(respuesta["estado"] == estado for respuesta in respuestas)
        for estado in ESTADOS
    }
    requiere_revision = bool(
        conteos["DUDOSA"]
        + conteos["DOBLE_MARCA"]
        or any(item["estado"] != "VALIDA" for item in dni)
        or any(
            item["estado"] in ("DUDOSA", "DOBLE_MARCA")
            for item in controles.values()
        )
    )
    return {
        "version": VERSION,
        "metodo": "fraccion_oscura_centro + KMeans (K=2) + guardas",
        "calibracion": calibracion,
        "resumen": {
            "preguntas_totales": len(respuestas),
            **conteos,
            "dni_completo": all(item["estado"] == "VALIDA" for item in dni),
            "requiere_revision": requiere_revision,
        },
        "dni": "".join(
            item["respuesta"] if item["estado"] == "VALIDA" else "?"
            for item in dni
        ),
        "detalle_dni": dni,
        "controles": controles,
        "respuestas": respuestas,
        "advertencia": (
            "EXPERIMENTAL. La confianza es heuristica. Verificar contra "
            "un conjunto de cartillas con respuestas conocidas antes de uso real."
        ),
    }

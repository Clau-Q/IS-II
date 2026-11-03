"""Comparación con plantilla vacía, marcas tenues y auditoría de decisiones."""

# ===================================================================
# MAPA DE REVISIÓN: pasos 8.2, 8.3, 8.4, 8.5, 8.6, 8.7
# Consulta 00_LEER_SECUENCIA.md para recorrer el algoritmo en orden.
# La numeración es documental; no cambia llamadas ni nombres Python.
# ===================================================================


from __future__ import annotations

from typing import Any
from collections.abc import Mapping
from collections.abc import Sequence
from .definir_parametros_omr import Burbuja, Diccionario, Imagen
from .medir_tinta_burbujas import _medir_burbujas, medir_circulo


# PASO 8.3 — Compara tinta detectada con la burbuja impresa vacía.
def medir_evidencia_plantilla(
    imagen_normalizada: Imagen,
    plantilla_normalizada: Imagen,
    burbujas: Mapping[str, Burbuja],
) -> dict[str, Diccionario]:
    """Mide diferencias con la misma burbuja impresa sin rellenar."""
    evidencia = {}
    for opcion, burbuja in burbujas.items():
        medicion_foto = medir_circulo(imagen_normalizada, burbuja)
        medicion_vacia = medir_circulo(plantilla_normalizada, burbuja)
        diferencia_contraste = (
            medicion_foto["contraste_local"]
            - medicion_vacia["contraste_local"]
        )
        diferencia_fraccion = (
            medicion_foto["fraccion_oscura"]
            - medicion_vacia["fraccion_oscura"]
        )
        evidencia[opcion] = {
            "incremento_contraste": round(diferencia_contraste, 2),
            "incremento_fraccion_oscura": round(diferencia_fraccion, 4),
            "fraccion_oscura": medicion_foto["fraccion_oscura"],
            "contraste_local": medicion_foto["contraste_local"],
            "fondo_local": medicion_foto["fondo_local"],
        }
    return evidencia


# PASO 8.2 — Intenta rescatar una marca tenue bajo criterios conservadores.
def rescatar_marca_tenue(
    resultado: Diccionario,
    lecturas_tres: Sequence[Mapping[str, Any]],
    burbujas: Mapping[str, Burbuja],
    imagen_normalizada: Imagen,
    plantilla_normalizada: Imagen,
    calibraciones_fiables: Mapping[str, bool],
) -> bool:
    """Rescata tentativamente una marca tenue y exige revisión manual.

    Las tres variantes provienen de la MISMA foto y no son verificaciones
    independientes. Solo se reconsidera una opción señalada por las tres.
    """
    if resultado["estado"] != "DUDOSA" or not all(
        calibraciones_fiables.values()
    ):
        return False
    if not all(
        lectura["estado"] == "DUDOSA" and len(lectura["candidatas"]) == 1
        for lectura in lecturas_tres
    ):
        return False

    opciones = [lectura["candidatas"][0] for lectura in lecturas_tres]
    if len(set(opciones)) != 1:
        return False
    candidata = opciones[0]
    otras = [opcion for opcion in burbujas if opcion != candidata]
    if candidata not in burbujas or not otras:
        return False

    mediciones_foto = _medir_burbujas(imagen_normalizada, burbujas)
    mediciones_vacias = _medir_burbujas(plantilla_normalizada, burbujas)
    incrementos_fraccion = {
        opcion: mediciones_foto[opcion]["fraccion_oscura"]
        - mediciones_vacias[opcion]["fraccion_oscura"]
        for opcion in burbujas
    }
    incrementos_contraste = {
        opcion: mediciones_foto[opcion]["contraste_local"]
        - mediciones_vacias[opcion]["contraste_local"]
        for opcion in burbujas
    }
    ventaja_fraccion = incrementos_fraccion[candidata] - max(
        incrementos_fraccion[opcion] for opcion in otras
    )
    ventaja_contraste = incrementos_contraste[candidata] - max(
        incrementos_contraste[opcion] for opcion in otras
    )
    resultado["diagnostico_marca_tenue"] = {
        "candidata": candidata,
        "fraccion_oscura": mediciones_foto[candidata]["fraccion_oscura"],
        "incremento_fraccion_vs_plantilla": round(
            incrementos_fraccion[candidata], 4
        ),
        "ventaja_fraccion_vs_otras": round(ventaja_fraccion, 4),
        "ventaja_contraste_vs_otras": round(ventaja_contraste, 2),
        "nota": "Umbrales experimentales: requieren validacion con cartillas reales",
    }
    aceptada = (
        mediciones_foto[candidata]["fraccion_oscura"] >= 0.54
        and incrementos_fraccion[candidata] >= 0.10
        and ventaja_fraccion >= 0.13
        and ventaja_contraste >= 20.0
    )
    if aceptada:
        resultado.update(
            estado="VALIDA",
            respuesta=candidata,
            candidatas=[candidata],
            confianza="baja",
            fuente_evidencia="rescate_marca_tenue_con_plantilla",
            requiere_revision_manual=True,
        )
    return aceptada


# PASO 8.5 — Clasifica intensidad de marcas moderadas y fuertes.
def _clasificar_evidencias(
    evidencia: Mapping[str, Diccionario], ranking: Sequence[str]
) -> tuple[list[str], list[str], list[str]]:
    """Devuelve opciones moderadas, fuertes y muy fuertes."""
    moderadas = []
    fuertes = []
    muy_fuertes = []
    for opcion in ranking:
        lectura = evidencia[opcion]
        contraste = lectura["incremento_contraste"]
        fraccion = lectura["incremento_fraccion_oscura"]
        oscuridad = lectura["fraccion_oscura"]
        if (contraste >= 8 and fraccion >= 0.20) or (
            contraste >= 14 and fraccion >= 0.14
        ):
            moderadas.append(opcion)
        if contraste >= 16 and fraccion >= 0.33 and oscuridad >= 0.70:
            fuertes.append(opcion)
        if contraste >= 20 and fraccion >= 0.37 and oscuridad >= 0.77:
            muy_fuertes.append(opcion)
    return moderadas, fuertes, muy_fuertes


# PASO 8.6 — Actualiza la decisión final y su motivo de auditoría.
def _escribir_decision_auditada(
    resultado: Diccionario,
    evidencia: Mapping[str, Diccionario],
    ranking: Sequence[str],
    estado: str,
    candidatas: Sequence[str],
    confianza: str,
    motivo: str,
    revision: bool = False,
) -> None:
    """Actualiza el resultado respetando el orden original de opciones."""
    indices = {opcion: indice for indice, opcion in enumerate(evidencia)}
    opciones_ordenadas = sorted(candidatas, key=indices.__getitem__)
    resultado.update(
        estado=estado,
        respuesta=(
            opciones_ordenadas[0]
            if estado == "VALIDA" and len(opciones_ordenadas) == 1
            else None
        ),
        candidatas=opciones_ordenadas,
        confianza=confianza,
        fuente_evidencia=motivo,
        requiere_revision_manual=bool(revision),
    )
    if estado != "SIN_RESPUESTA":
        resultado["mejor_alternativa"] = (
            opciones_ordenadas[0] if opciones_ordenadas else ranking[0]
        )


# PASO 8.7 — Conserva marcas dominantes pese a diferencias bajo sombra.
def _consenso_fuerte_bajo_sombra(
    resultado: Mapping[str, Any], opcion: str | None
) -> bool:
    """Detecta una marca dominante pese a diferencias débiles con plantilla."""
    mediciones = resultado.get("mediciones", {})
    fraccion = (
        mediciones.get(opcion, {}).get("fraccion_oscura", 0)
        if opcion
        else 0
    )
    return bool(
        resultado.get("confianza") == "alta"
        and opcion
        and fraccion >= 0.83
        and resultado.get("margen", 0) >= 0.49
        and len(resultado.get("candidatas", [])) == 1
    )


# PASO 8.10 — Distingue una marca dominante del ruido moderado de impresión.
def _marca_dominante_verificable(
    resultado: Mapping[str, Any],
    evidencia: Mapping[str, Diccionario],
    ranking: Sequence[str],
    fuertes: Sequence[str],
    *,
    tipo: str,
) -> Diccionario | None:
    """Propone marca única solo cuando hay ventaja física Y acuerdo de lecturas.

    Un segundo incremento moderado puede proceder de letras, sombra o un
    pequeño desregistro entre imágenes. No se elimina una DOBLE_MARCA fuerte
    ni se aplica a DNI/controles (son problemas de clasificación diferentes).
    Los tres tratamientos están correlacionados: el acuerdo nunca se trata
    como evidencia independiente ni como probabilidad de acierto.
    """
    if tipo != "pregunta" or not ranking or len(fuertes) > 1:
        return None

    candidata = ranking[0]
    medida = evidencia[candidata]
    restantes = [evidencia[op] for op in ranking[1:]]
    if not restantes:
        return None
    mas_oscura = max(restantes, key=lambda e: e["fraccion_oscura"])
    siguiente_contraste = evidencia[ranking[1]]["incremento_contraste"]
    margen_contraste = medida["incremento_contraste"] - siguiente_contraste
    margen_fraccion = medida["fraccion_oscura"] - mas_oscura["fraccion_oscura"]
    incremento_otro_max = max(e["incremento_fraccion_oscura"] for e in restantes)

    # Correlación con resultado previo, que se debe haber obtenido antes de
    # la auditoría por diferencias. No convertir discrepancias en aciertos.
    if resultado["estado"] == "DOBLE_MARCA":
        return None
    if resultado["estado"] == "VALIDA" and resultado.get("respuesta") != candidata:
        return None
    validaciones = resultado.get("validaciones", {})
    votos = sum(
        v.get("estado") == "VALIDA" and v.get("respuesta") == candidata
        for v in validaciones.values()
    )
    desacuerdos = any(
        v.get("estado") == "VALIDA" and v.get("respuesta") != candidata
        for v in validaciones.values()
    )
    if desacuerdos or votos < 2:
        return None

    # Valores experimentales conservadores, pendientes de calibrar con
    # etiquetas de respuesta real. Evitan que una segunda marca visible sea
    # desechada simplemente porque la primera sea más oscura.
    es_clara = (
        medida["contraste_local"] >= 25
        and medida["incremento_contraste"] >= 32
        and medida["incremento_fraccion_oscura"] >= 0.30
        and medida["fraccion_oscura"] >= 0.72
        and margen_contraste >= 26
        and margen_fraccion >= 0.20
        and mas_oscura["fraccion_oscura"] <= 0.60
        and incremento_otro_max <= 0.30
    )
    # Rescate más limitado para tinta tenue: exige segunda burbuja muy clara
    # y diferencia marcada respecto a la plantilla vacía.
    es_tenue_aislada = (
        medida["incremento_contraste"] >= 26
        and medida["incremento_fraccion_oscura"] >= 0.28
        and medida["fraccion_oscura"] >= 0.62
        and margen_contraste >= 24
        and margen_fraccion >= 0.28
        and mas_oscura["fraccion_oscura"] <= 0.39
        and incremento_otro_max <= 0.19
    )
    if not (es_clara or es_tenue_aislada):
        return None

    return {
        "opcion": candidata,
        "motivo": "marca_dominante_con_evidencia_local" if es_clara
                  else "marca_tenue_aislada_con_evidencia_local",
        "margen_contraste": round(margen_contraste, 2),
        "margen_fraccion": round(margen_fraccion, 4),
        "votos_variantes_correlacionadas": votos,
        "advertencia": "Criterios heurísticos; no equivalen a acierto demostrado",
    }


# PASO 8.4 — Reevalúa la decisión inicial frente a evidencia de plantilla.
def auditar_opciones_con_plantilla(
    resultado: Diccionario,
    evidencia: Mapping[str, Diccionario],
    *,
    tipo: str = "pregunta",
) -> Diccionario:
    """Valida la clasificación inicial usando tinta añadida a la plantilla.

    ``tipo`` permanece para compatibilidad. Las confianzas son heurísticas.
    Esta función modifica ``resultado`` y devuelve la misma referencia.
    """
    estado_anterior = resultado["estado"]
    respuesta_anterior = resultado.get("respuesta")
    ranking = sorted(
        evidencia,
        key=lambda opcion: evidencia[opcion]["incremento_contraste"],
        reverse=True,
    )
    moderadas, fuertes, muy_fuertes = _clasificar_evidencias(
        evidencia, ranking
    )
    # 8.10 — Priorizar una marca dominante frente a otros incrementos
    # moderados (sin descartar dobles realmente fuertes).
    dominancia = _marca_dominante_verificable(
        resultado, evidencia, ranking, fuertes, tipo=tipo
    )
    resultado.update(
        evidencia_plantilla=evidencia,
        candidatas_evidencia=moderadas,
        estado_previo=estado_anterior,
        requiere_revision_manual=False,
    )

    def escribir(
        estado: str,
        candidatas: Sequence[str],
        confianza: str,
        motivo: str,
        revision: bool = False,
    ) -> None:
        _escribir_decision_auditada(
            resultado, evidencia, ranking, estado,
            candidatas, confianza, motivo, revision,
        )

    if len(muy_fuertes) >= 2:
        escribir(
            "DOBLE_MARCA", muy_fuertes, "alta", "doble_marca_fuerte_confirmada"
        )
    elif len(fuertes) >= 2:
        escribir("DOBLE_MARCA", fuertes, "media", "doble_marca_posible", True)
    elif dominancia is not None:
        escribir("VALIDA", [dominancia["opcion"]], "media",
                 dominancia["motivo"])
        resultado["diagnostico_dominancia"] = dominancia
    elif len(moderadas) >= 2:
        escribir(
            "DUDOSA", moderadas, "baja", "multiples_marcas_una_tenue", True
        )
    elif len(fuertes) == 1:
        unica = fuertes[0]
        if estado_anterior == "DOBLE_MARCA" or (
            respuesta_anterior and respuesta_anterior != unica
        ):
            candidatas = list(
                dict.fromkeys([unica] + resultado.get("candidatas", []))
            )
            escribir(
                "DUDOSA", candidatas, "baja",
                "discordancia_con_detector_original", True,
            )
        elif estado_anterior in ("DUDOSA", "SIN_RESPUESTA"):
            escribir("VALIDA", [unica], "media", "marca_robusta_con_plantilla")
        else:
            confianza = (
                "alta"
                if unica in muy_fuertes and resultado.get("confianza") == "alta"
                else "media"
            )
            escribir("VALIDA", [unica], confianza, "consenso_con_plantilla")
    elif resultado.get("fuente_evidencia") == "rescate_marca_tenue_con_plantilla":
        # No deshacer rescates anteriores, pero siempre requieren revisión.
        resultado["requiere_revision_manual"] = True
        resultado["confianza"] = "baja"
    elif moderadas:
        unica = moderadas[0]
        if (
            len(moderadas) == 1
            and estado_anterior == "VALIDA"
            and respuesta_anterior == unica
            and _consenso_fuerte_bajo_sombra(resultado, unica)
        ):
            escribir(
                "VALIDA", [unica], "media",
                "consenso_fuerte_con_plantilla_bajo_sombra",
            )
        else:
            escribir("DUDOSA", moderadas, "baja", "marca_tenue_o_parcial", True)
    elif estado_anterior == "VALIDA":
        if _consenso_fuerte_bajo_sombra(resultado, respuesta_anterior):
            escribir(
                "VALIDA", [respuesta_anterior], "media",
                "consenso_fuerte_en_foto_bajo_sombra",
            )
        else:
            candidatas = (
                [respuesta_anterior]
                if respuesta_anterior
                else resultado.get("candidatas", [])
            )
            escribir(
                "DUDOSA", candidatas, "baja",
                "discrepancia_foto_plantilla", True,
            )
    elif estado_anterior == "DOBLE_MARCA":
        escribir(
            "DUDOSA", resultado.get("candidatas", []), "baja",
            "doble_sin_evidencia_suficiente", True,
        )
    else:
        escribir("SIN_RESPUESTA", [], "alta", "sin_tinta_anadida_consistente")

    return resultado

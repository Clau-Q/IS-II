"""Fusión, auditoría y resumen final de las lecturas de las cartillas."""

# ===================================================================
# MAPA DE REVISIÓN: pasos 7.1, 7.2, 8.1, 8.8, 8.9, 9.1, 9.2, 9.3, 9.5
# Consulta 00_LEER_SECUENCIA.md para recorrer el algoritmo en orden.
# La numeración es documental; no cambia llamadas ni nombres Python.
# ===================================================================


from __future__ import annotations

from typing import Any
from collections.abc import Mapping
from collections.abc import Sequence
from .auditar_marcas_con_plantilla import auditar_opciones_con_plantilla, medir_evidencia_plantilla, rescatar_marca_tenue
from .clasificar_respuestas_dni_area import leer
from .definir_parametros_omr import Diccionario, ESTADOS, Imagen, SECCIONES_CONTROL, TOTAL_COLUMNAS_DNI, TOTAL_PREGUNTAS, UMBRAL_FOCO, VERSION
from .consensuar_lecturas import combinar_opciones
from .normalizar_luz_fotografia import evaluar_calidad, normalizar_luz, tratamientos


# PASO 7.1 — Elige los dos tratamientos que se compararán.
def _seleccionar_variantes(
    lecturas: Mapping[str, Diccionario],
) -> tuple[str, str, str, str]:
    """Elige el par de normalizaciones según calibración y marcas válidas."""
    fiables = {
        nombre: bool(lectura["calibracion"]["dos_grupos_fiables"])
        for nombre, lectura in lecturas.items()
    }
    validas_suave = lecturas["suave"]["resumen"]["VALIDA"]
    validas_contraste = lecturas["contraste"]["resumen"]["VALIDA"]

    variante_a = "suave"
    variante_b = "contraste"
    motivo = "Consenso habitual entre normalizacion suave y contraste"
    if (
        fiables["contraste"]
        and fiables["respaldo"]
        and (
            not fiables["suave"]
            or (
                validas_contraste >= 10
                and validas_suave < 0.80 * validas_contraste
            )
        )
    ):
        variante_a = "contraste"
        variante_b = "respaldo"
        motivo = "Consenso entre contraste y respaldo, por calibracion adaptativa"

    tercero = next(
        nombre for nombre in lecturas if nombre not in (variante_a, variante_b)
    )
    return variante_a, variante_b, tercero, motivo


# PASO 7.2 — Exige 90 respuestas y ocho columnas de DNI.
def _verificar_cantidades(
    lecturas: Sequence[Mapping[str, Any]], datos: Mapping[str, Any]
) -> None:
    if not all(
        len(lectura["respuestas"]) == len(datos["respuestas"]) == TOTAL_PREGUNTAS
        for lectura in lecturas
    ):
        raise ValueError("Las tres lecturas deben devolver exactamente 90 preguntas")
    if not all(
        len(lectura["detalle_dni"])
        == len(datos["dni"])
        == TOTAL_COLUMNAS_DNI
        for lectura in lecturas
    ):
        raise ValueError(
            "Las tres lecturas deben devolver exactamente ocho columnas DNI"
        )


# PASO 8.1 — Aplica consenso, rescate y auditoría a cada pregunta.
def _fusionar_respuestas(
    lecturas: Mapping[str, Diccionario],
    variante_a: str,
    variante_b: str,
    tercero: str,
    datos: Mapping[str, Any],
    foto_suave: Imagen,
    plantilla_suave: Imagen,
    fiables: Mapping[str, bool],
    rescatar_tenues: bool,
) -> list[Diccionario]:
    respuestas = []
    columnas_a = lecturas[variante_a]["respuestas"]
    columnas_b = lecturas[variante_b]["respuestas"]
    columnas_c = lecturas[tercero]["respuestas"]

    for indice, (lectura_a, lectura_b, lectura_c) in enumerate(
        zip(columnas_a, columnas_b, columnas_c)
    ):
        resultado = combinar_opciones(
            lectura_a, lectura_b, lectura_c, variante_a, variante_b
        )
        resultado["pregunta"] = lectura_a["pregunta"]
        burbujas = datos["respuestas"][indice]["opciones"]

        if rescatar_tenues:
            diagnosticos = tuple(
                lecturas[nombre]["respuestas"][indice]
                for nombre in ("suave", "contraste", "respaldo")
            )
            rescatar_marca_tenue(
                resultado,
                diagnosticos,
                burbujas,
                foto_suave,
                plantilla_suave,
                fiables,
            )

        evidencia = medir_evidencia_plantilla(
            foto_suave, plantilla_suave, burbujas
        )
        respuestas.append(auditar_opciones_con_plantilla(resultado, evidencia))

    return respuestas


# PASO 8.8 — Aplica consenso y auditoría a ocho columnas DNI.
def _fusionar_dni(
    lecturas: Mapping[str, Diccionario],
    variante_a: str,
    variante_b: str,
    tercero: str,
    datos: Mapping[str, Any],
    foto_suave: Imagen,
    plantilla_suave: Imagen,
) -> list[Diccionario]:
    dni = []
    lecturas_a = lecturas[variante_a]["detalle_dni"]
    lecturas_b = lecturas[variante_b]["detalle_dni"]
    lecturas_c = lecturas[tercero]["detalle_dni"]
    for indice, (lectura_a, lectura_b, lectura_c) in enumerate(
        zip(lecturas_a, lecturas_b, lecturas_c), start=1
    ):
        resultado = combinar_opciones(
            lectura_a, lectura_b, lectura_c, variante_a, variante_b
        )
        resultado["columna"] = indice
        burbujas = datos["dni"][indice - 1]["digitos"]
        evidencia = medir_evidencia_plantilla(
            foto_suave, plantilla_suave, burbujas
        )
        dni.append(
            auditar_opciones_con_plantilla(resultado, evidencia, tipo="dni")
        )
    return dni


# PASO 8.9 — Aplica consenso y auditoría al turno, área y tema.
def _fusionar_controles(
    lecturas: Mapping[str, Diccionario],
    variante_a: str,
    variante_b: str,
    tercero: str,
    datos: Mapping[str, Any],
    foto_suave: Imagen,
    plantilla_suave: Imagen,
) -> dict[str, Diccionario]:
    controles = {}
    for seccion in SECCIONES_CONTROL:
        resultado = combinar_opciones(
            lecturas[variante_a]["controles"][seccion],
            lecturas[variante_b]["controles"][seccion],
            lecturas[tercero]["controles"][seccion],
            variante_a,
            variante_b,
        )
        evidencia = medir_evidencia_plantilla(
            foto_suave, plantilla_suave, datos[seccion]
        )
        controles[seccion] = auditar_opciones_con_plantilla(
            resultado, evidencia, tipo="control"
        )
    return controles


# PASO 9.2 — Comprueba ausencia global de marcas medibles.
def _es_hoja_vacia_probable(
    respuestas: Sequence[Diccionario],
    dni: Sequence[Diccionario],
    controles: Mapping[str, Diccionario],
) -> bool:
    """Busca ausencia global de tinta medible, no solo K-Means poco fiable."""
    evidencias = [
        medida
        for respuesta in respuestas
        for medida in respuesta["evidencia_plantilla"].values()
    ]
    potenciales = sum(
        medida["incremento_contraste"] >= 8
        and medida["incremento_fraccion_oscura"] >= 0.20
        for medida in evidencias
    )
    marcas_identificacion = sum(
        item["estado"] in ("VALIDA", "DOBLE_MARCA")
        for item in [*dni, *controles.values()]
    )
    respuestas_sin_marcas = all(
        item["estado"] not in ("VALIDA", "DOBLE_MARCA")
        for item in respuestas
    )
    return potenciales == 0 and marcas_identificacion == 0 and respuestas_sin_marcas


# PASO 9.3 — Corrige dudas falsas cuando la hoja parece vacía.
def _ajustar_hoja_vacia(
    respuestas: list[Diccionario],
    dni: list[Diccionario],
    controles: Mapping[str, Diccionario],
) -> None:
    """Evita clasificar todas las burbujas vacías como falsos dudosos."""
    for item in [*respuestas, *dni, *controles.values()]:
        if (
            item["estado"] == "DUDOSA"
            and item["fuente_evidencia"]
            != "rescate_marca_tenue_con_plantilla"
        ):
            item.update(
                estado="SIN_RESPUESTA",
                candidatas=[],
                respuesta=None,
                confianza="baja",
                requiere_revision_manual=False,
                fuente_evidencia="hoja_vacia_probable_sin_tinta_medible",
            )


# PASO 9.5 — Reúne conteos, revisiones y aptitud provisional.
def _resumen_consolidado(
    respuestas: Sequence[Diccionario],
    dni: Sequence[Diccionario],
    controles: Mapping[str, Diccionario],
    calidad: Mapping[str, Any],
    hoja_vacia: bool,
) -> Diccionario:
    conteos = {
        estado: sum(item["estado"] == estado for item in respuestas)
        for estado in ESTADOS
    }
    preguntas_revision = [
        item["pregunta"]
        for item in respuestas
        if item["requiere_revision_manual"]
    ]
    dobles_confirmadas = [
        item["pregunta"]
        for item in respuestas
        if item["estado"] == "DOBLE_MARCA"
        and not item["requiere_revision_manual"]
    ]
    dobles_pendientes = [
        item["pregunta"]
        for item in respuestas
        if item["estado"] == "DOBLE_MARCA"
        and item["requiere_revision_manual"]
    ]
    marcas_rescatadas = [
        item["pregunta"]
        for item in respuestas
        if item["estado"] == "VALIDA"
        and item.get("fuente_evidencia")
        == "rescate_marca_tenue_con_plantilla"
    ]
    # PASO 8.10 — Registrar cuáles marcas se resolvieron por dominancia
    # de tinta y nunca confundirlas con exactitud medida en un examen.
    dominancias = [
        item["pregunta"] for item in respuestas
        if item["estado"] == "VALIDA" and item.get("diagnostico_dominancia")
    ]
    dni_revision = [
        item["columna"] for item in dni if item["requiere_revision_manual"]
    ]
    controles_revision = [
        nombre
        for nombre, item in controles.items()
        if item["requiere_revision_manual"]
    ]
    dni_completo = all(item["estado"] == "VALIDA" for item in dni)
    identificacion_completa = dni_completo and all(
        item["estado"] == "VALIDA" for item in controles.values()
    )
    revision_calidad = bool(
        (hoja_vacia and calidad["advertencias"])
        or calidad["varianza_laplaciano_mitad"] < UMBRAL_FOCO
    )
    requiere_revision = bool(
        preguntas_revision
        or dni_revision
        or controles_revision
        or revision_calidad
    )
    return {
        "preguntas_totales": len(respuestas),
        **conteos,
        "hoja_vacia_probable": bool(hoja_vacia),
        "dobles_confirmadas_sin_revision": dobles_confirmadas,
        "dobles_pendientes_revision": dobles_pendientes,
        "preguntas_revision": preguntas_revision,
        "marcas_tenues_rescatadas": marcas_rescatadas,
        "cantidad_marcas_tenues": len(marcas_rescatadas),
        "preguntas_resueltas_por_dominancia": dominancias,
        "cantidad_resueltas_por_dominancia": len(dominancias),
        "dni_completo": dni_completo,
        "dni_columnas_revision": dni_revision,
        "controles_revision": controles_revision,
        "dni_faltantes_o_invalidos": [
            item["columna"] for item in dni if item["estado"] != "VALIDA"
        ],
        "controles_faltantes_o_invalidos": [
            nombre
            for nombre, item in controles.items()
            if item["estado"] != "VALIDA"
        ],
        "datos_identificacion_completos": identificacion_completa,
        "revision_global_calidad": revision_calidad,
        "requiere_revision": requiere_revision,
        "lectura_apta_para_calificar": (
            not requiere_revision and identificacion_completa and not hoja_vacia
        ),
    }


# PASO 9.1 — Orquestador de lectura: llama a las etapas 4–9; se invoca desde 1.2.
def leer_v4(
    gris: Imagen,
    datos: Mapping[str, Any],
    referencia: Imagen,
    rescatar_tenues: bool = True,
) -> Diccionario:
    """Lee una hoja con consenso, rescate conservador y auditoría visual."""
    # 4.1 — Generar los tres tratamientos de la misma foto.
    variantes = tratamientos(gris)
    # 5–6 — Medir y clasificar las burbujas en cada tratamiento.
    lecturas = {
        nombre: leer(imagen, datos, referencia)
        for nombre, imagen in variantes.items()
    }
    # 7.1 — Seleccionar variantes para consenso.
    variante_a, variante_b, tercero, motivo = _seleccionar_variantes(lecturas)
    lectura_a = lecturas[variante_a]
    lectura_b = lecturas[variante_b]
    lectura_c = lecturas[tercero]
    _verificar_cantidades((lectura_a, lectura_b, lectura_c), datos)

    calibraciones_fiables = {
        nombre: bool(lectura["calibracion"]["dos_grupos_fiables"])
        for nombre, lectura in lecturas.items()
    }
    foto_suave = variantes["suave"]
    plantilla_suave = normalizar_luz(referencia, "suave")
    # 8.1 — Revisar preguntas con consenso y evidencia de plantilla.
    respuestas = _fusionar_respuestas(
        lecturas, variante_a, variante_b, tercero, datos,
        foto_suave, plantilla_suave, calibraciones_fiables, rescatar_tenues,
    )
    # 8.8 — Fusionar las ocho columnas DNI.
    dni = _fusionar_dni(
        lecturas, variante_a, variante_b, tercero, datos,
        foto_suave, plantilla_suave,
    )
    # 8.9 — Fusionar turno, área y tema.
    controles = _fusionar_controles(
        lecturas, variante_a, variante_b, tercero, datos,
        foto_suave, plantilla_suave,
    )

    # 9.2 — Detectar hoja probablemente vacía.
    hoja_vacia = _es_hoja_vacia_probable(respuestas, dni, controles)
    # 9.4 — Evaluar calidad de captura.
    calidad = evaluar_calidad(gris)
    if hoja_vacia:
        _ajustar_hoja_vacia(respuestas, dni, controles)

    # 9.5 — Producir decisión y resumen final de lectura.
    resumen = _resumen_consolidado(
        respuestas, dni, controles, calidad, hoja_vacia
    )
    conteos_variantes = {
        nombre: lectura["resumen"]["VALIDA"]
        for nombre, lectura in lecturas.items()
    }
    return {
        "version": VERSION,
        "metodo": (
            "normalizacion local + 3 tratamientos + contraste "
            "contra plantilla + confirmacion dobles"
        ),
        "calibracion": {
            nombre: lectura["calibracion"]
            for nombre, lectura in lecturas.items()
        },
        "estrategia": {
            "tratamientos_aceptacion": [variante_a, variante_b],
            "tratamiento_diagnostico": tercero,
            "motivo": motivo,
            "cantidad_validas_por_metodo": conteos_variantes,
            "grupos_fiables": calibraciones_fiables,
            "advertencia": (
                "Los tratamientos de una misma foto NO son pruebas independientes"
            ),
        },
        "calidad_imagen": calidad,
        "resumen": resumen,
        "dni": "".join(
            item["respuesta"] if item["estado"] == "VALIDA" else "?"
            for item in dni
        ),
        "detalle_dni": dni,
        "controles": controles,
        "respuestas": respuestas,
        "advertencia": (
            "Prototipo no validado con verdad terreno. DOBLE_MARCA "
            "de confianza alta no exige revision manual, pero invalida "
            "la pregunta segun las reglas del examen."
        ),
    }

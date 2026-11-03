"""Flujo de procesamiento completo desde imagen hasta reporte."""

# ===================================================================
# MAPA DE REVISIÓN: pasos 1.2
# Consulta 00_LEER_SECUENCIA.md para recorrer el algoritmo en orden.
# La numeración es documental; no cambia llamadas ni nombres Python.
# ===================================================================


from __future__ import annotations

from pathlib import Path
import cv2
import hashlib
from .alinear_fotografia import alinear, mejora_ecc
from .validar_cuadricula_respuestas import verificar_cuadricula
from .definir_parametros_omr import Diccionario, UMBRAL_ERROR_ALINEACION
from .consolidar_resultados_omr import leer_v4
from .cargar_plantilla_referencia import _leer_imagen, leer_datos
from .exportar_json_csv import _guardar_resultados


# PASO 1.2 — Coordinador principal: plantilla, alineación opcional, lectura y archivos.
def procesar(
    ruta: str | Path,
    carpeta: str | Path,
    salida: str | Path | None = None,
    alineacion: bool = False,
    refinar: bool = False,
    rescatar_tenues: bool = True,
    comparar_clusters: bool = False,
    alineacion_local: bool = False,
) -> Diccionario:
    """Ejecuta el flujo OMR y guarda archivos compatibles con v0.5."""
    ruta = Path(ruta)
    carpeta = Path(carpeta)
    # 2.1 — Cargar plantilla validada y coordenadas.
    datos, referencia = leer_datos(carpeta)
    reporte = None
    ruta_procesada = ruta

    # 3.1 — Alinear la fotografía solo si se solicita.
    if alineacion:
        identificador = hashlib.sha1(
            str(ruta.resolve()).encode("utf-8")
        ).hexdigest()[:12]
        prefijo_alineacion = f"temp_v4_{identificador}"
        reporte = alinear(ruta, carpeta, prefijo=prefijo_alineacion,
                          alineacion_local=alineacion_local)
        if not reporte.get("valido", False):
            return {
                "exito": False,
                "error": "Alineacion rechazada: " + reporte.get("motivo", "sin diagnostico"),
                "reporte_alineacion": reporte,
            }
        ruta_procesada = carpeta / f"{prefijo_alineacion}_alineada.png"

    gris = _leer_imagen(ruta_procesada, cv2.IMREAD_GRAYSCALE)
    if gris.shape != referencia.shape:
        raise ValueError(
            f"Tamaño de imagen {gris.shape[::-1]} no coincide "
            f"con plantilla {referencia.shape[::-1]}"
        )

    informacion_ecc = {"aplicado": False, "motivo": "No solicitado"}
    # 3.6 — Refinamiento geométrico ECC opcional.
    if refinar and not (reporte and (
        reporte.get("metricas", {}).get("ecc_automatico")
        or reporte.get("metricas", {}).get("alineacion_local")
    )):
        gris, informacion_ecc = mejora_ecc(gris, referencia, datos)
    elif reporte and reporte.get("metricas", {}).get("ecc_automatico"):
        informacion_ecc = dict(reporte["metricas"]["ecc_automatico"])
        informacion_ecc["motivo"] = "Refinamiento ECC automático durante la alineación"

    # PASO 3.9 — También controlar las hojas proporcionadas YA alineadas y
    # repetir el control tras un ECC opcional: una imagen de tamaño correcto
    # no implica que el centro de las burbujas sea correcto.
    if datos.get("marcadores_px"):
        verificacion = verificar_cuadricula(gris, referencia, datos)
        if not verificacion["valido"]:
            return {"exito": False, "error": "Desalineacion de burbujas: "
                    + verificacion["motivo"],
                    "verificacion_geometrica": verificacion,
                    "reporte_alineacion": reporte}
    else:
        verificacion = {"valido": False,
                        "motivo": "Sin marcadores en las coordenadas: lectura sin verificacion geometrica"}

    # 9.1 — Entrar al lector que orquesta las etapas 4, 5, 6, 7, 8 y 9.
    resultado = leer_v4(
        gris, datos, referencia, rescatar_tenues=rescatar_tenues
    )
    if reporte and reporte.get("valido"):
        error_mediano = reporte.get("metricas", {}).get("error_mediano_px", 0)
        if (error_mediano > UMBRAL_ERROR_ALINEACION
                or reporte.get("revision_geometrica_recomendada", False)):
            resultado["resumen"]["requiere_revision"] = True
            resultado["resumen"]["revision_global_alineacion"] = True
            # Evita el estado contradictorio de la versión original.
            resultado["resumen"]["lectura_apta_para_calificar"] = False

    if not verificacion["valido"]:
        resultado["resumen"]["requiere_revision"] = True
        resultado["resumen"]["revision_global_alineacion"] = True
        resultado["resumen"]["lectura_apta_para_calificar"] = False
    resultado["verificacion_geometrica"] = verificacion
    resultado["imagen_fuente"] = ruta.name
    resultado["reporte_alineacion"] = reporte
    resultado["refinamiento_ecc"] = informacion_ecc
    prefijo_salida = (
        Path(salida) if salida is not None else carpeta / f"{ruta.stem}_omr_v4"
    )
    # ETAPA 09.2 — Diagnóstico experimental (opcional); NO cambia estados OMR.
    if comparar_clusters:
        try:
            from .debug_comparar_algoritmos_agrupamiento import (
                comparar_agrupamientos, guardar_comparacion_csv
            )
        except ModuleNotFoundError as error:
            if error.name != __package__ + ".debug_comparar_algoritmos_agrupamiento":
                raise
            raise RuntimeError(
                "La comparación experimental requiere el módulo "
                "09_2_debug_comparar_algoritmos_agrupamiento.py"
            ) from error
        resultado['comparador_clusters'] = comparar_agrupamientos(resultado)
        guardar_comparacion_csv(
            str(prefijo_salida) + '_comparacion_clusters.csv',
            resultado['comparador_clusters'],
        )
    # 10.1 — Guardar resultados y revisión visual.
    _guardar_resultados(prefijo_salida, gris, datos, resultado)
    return resultado

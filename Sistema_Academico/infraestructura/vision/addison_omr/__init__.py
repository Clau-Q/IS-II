"""API pública del lector ADDISON OMR (versión experimental)."""

# FACHADA PÚBLICA — reexporta funciones de las etapas 1–10.

# Los nombres numerados son cómodos para estudiar el orden, pero Python
# no admite usar "from .03_alineacion import ..." en una instrucción import.
# Este buscador enlaza los nombres internos originales con los archivos numerados,
# sin duplicar módulos ni alterar la lógica del lector.
from importlib.abc import MetaPathFinder as _MetaPathFinder
from importlib.util import spec_from_file_location as _spec_from_file_location
from pathlib import Path as _Path
from sys import meta_path as _meta_path

_ARCHIVOS_POR_MODULO = {
    "definir_parametros_omr": "00_definir_parametros_omr.py",
    "recibir_argumentos_cli": "01_1_recibir_argumentos_cli.py",
    "ejecutar_flujo_lectura": "01_2_ejecutar_flujo_lectura.py",
    "cargar_plantilla_referencia": "02_1_cargar_plantilla_referencia.py",
    "localizar_burbujas": "02_4_localizar_burbujas.py",
    "alinear_fotografia": "03_1_alinear_fotografia.py",
    "detectar_marcadores_esquinas": "03_2_detectar_marcadores_esquinas.py",
    "corregir_alineacion_local": "03_4_corregir_alineacion_local.py",
    "validar_cuadricula_respuestas": "03_3_validar_cuadricula_respuestas.py",
    "normalizar_luz_fotografia": "04_normalizar_luz_fotografia.py",
    "medir_tinta_burbujas": "05_medir_tinta_burbujas.py",
    "clasificar_respuestas_dni_area": "06_clasificar_respuestas_dni_area.py",
    "consensuar_lecturas": "07_consensuar_lecturas.py",
    "auditar_marcas_con_plantilla": "08_auditar_marcas_con_plantilla.py",
    "consolidar_resultados_omr": "09_1_consolidar_resultados_omr.py",
    "debug_comparar_algoritmos_agrupamiento": "09_2_debug_comparar_algoritmos_agrupamiento.py",
    "comparar_varias_fotos_cartilla": "11_1_comparar_varias_fotos_cartilla.py",
    "exportar_json_csv": "10_1_exportar_json_csv.py",
    "debug_dibujar_imagen_revision": "10_2_debug_dibujar_imagen_revision.py",
    # Alias anteriores, conservados para compatibilidad.
    "config": "00_definir_parametros_omr.py",
    "cli": "01_1_recibir_argumentos_cli.py",
    "pipeline": "01_2_ejecutar_flujo_lectura.py",
    "plantilla": "02_1_cargar_plantilla_referencia.py",
    "coordenadas": "02_4_localizar_burbujas.py",
    "alineacion": "03_1_alinear_fotografia.py",
    "marcadores": "03_2_detectar_marcadores_esquinas.py",
    "alineacion_local": "03_4_corregir_alineacion_local.py",
    "verificacion_geometrica": "03_3_validar_cuadricula_respuestas.py",
    "preprocesamiento": "04_normalizar_luz_fotografia.py",
    "medicion": "05_medir_tinta_burbujas.py",
    "clasificacion": "06_clasificar_respuestas_dni_area.py",
    "consenso": "07_consensuar_lecturas.py",
    "auditoria": "08_auditar_marcas_con_plantilla.py",
    "consolidacion": "09_1_consolidar_resultados_omr.py",
    "agrupamiento_experimental": "09_2_debug_comparar_algoritmos_agrupamiento.py",
    "recuperacion_lote": "11_1_comparar_varias_fotos_cartilla.py",
    "reportes": "10_1_exportar_json_csv.py",
    "visualizacion": "10_2_debug_dibujar_imagen_revision.py",
}


class _BuscadorModulosNumerados(_MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        prefijo = __name__ + "."
        if not fullname.startswith(prefijo):
            return None
        nombre = fullname[len(prefijo):]
        archivo = _ARCHIVOS_POR_MODULO.get(nombre)
        if archivo is None:
            return None
        ruta_modulo = _Path(__file__).parent / archivo
        # Si se eliminan los módulos debug, no intentamos cargarlos.
        if not ruta_modulo.is_file():
            return None
        return _spec_from_file_location(fullname, ruta_modulo)


_meta_path.insert(0, _BuscadorModulosNumerados())


from .alinear_fotografia import alinear, mejora_ecc, medidas_homografia, extraer_coincidencias
from .auditar_marcas_con_plantilla import medir_evidencia_plantilla, rescatar_marca_tenue, auditar_opciones_con_plantilla
from .clasificar_respuestas_dni_area import kmeans_umbral, resolver_opciones, resolver_controles, leer
from .recibir_argumentos_cli import main
from .definir_parametros_omr import VERSION, TOTAL_PREGUNTAS, TOTAL_COLUMNAS_DNI, SECCIONES_CONTROL, ESTADOS
from .consensuar_lecturas import consenso_item, combinar_opciones
from .consolidar_resultados_omr import leer_v4
from .medir_tinta_burbujas import medir_circulo
from .ejecutar_flujo_lectura import procesar
from .cargar_plantilla_referencia import leer_datos, guardar_json
from .normalizar_luz_fotografia import normalizar_luz, tratamientos, evaluar_calidad


__all__ = ['VERSION', 'TOTAL_PREGUNTAS', 'TOTAL_COLUMNAS_DNI', 'SECCIONES_CONTROL', 'ESTADOS', 'leer_datos', 'alinear', 'mejora_ecc', 'medir_circulo', 'medidas_homografia', 'extraer_coincidencias', 'kmeans_umbral', 'resolver_opciones', 'resolver_controles', 'leer', 'normalizar_luz', 'tratamientos', 'evaluar_calidad', 'consenso_item', 'combinar_opciones', 'medir_evidencia_plantilla', 'rescatar_marca_tenue', 'auditar_opciones_con_plantilla', 'leer_v4', 'guardar_json', 'procesar', 'main']



# Diagnósticos opcionales: no deben impedir importar el lector si se borran.
try:
    from .debug_dibujar_imagen_revision import anotacion
except ModuleNotFoundError as error:
    if error.name != __name__ + ".debug_dibujar_imagen_revision":
        raise
else:
    __all__.append("anotacion")

try:
    from .debug_comparar_algoritmos_agrupamiento import comparar_agrupamientos
except ModuleNotFoundError as error:
    if error.name != __name__ + ".debug_comparar_algoritmos_agrupamiento":
        raise
else:
    __all__.append("comparar_agrupamientos")

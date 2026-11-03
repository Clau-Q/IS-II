"""ADDISON OMR v0.5: lectura experimental de cartillas con plantilla.

Dependencias::

    pip install numpy opencv-python

La carpeta de plantilla debe contener
``02_3_plantilla_maestra_sin_marcas.png`` y
``02_2_mapa_coordenadas_burbujas.json`` (también se admiten los nombres anteriores).

Ejemplo::

    python -m addison_omr foto.jpg --carpeta addison_omr --alinear

Los indicadores de confianza son heurísticos, no probabilidades calibradas.
Es imprescindible validar el lector con cartillas de respuesta conocida."""

# ===================================================================
# MAPA DE REVISIÓN: pasos 1.1
# Consulta 00_LEER_SECUENCIA.md para recorrer el algoritmo en orden.
# La numeración es documental; no cambia llamadas ni nombres Python.
# ===================================================================


from __future__ import annotations

from pathlib import Path
from collections.abc import Sequence
import argparse
from .ejecutar_flujo_lectura import procesar


# PASO 1.1 — Entrada CLI: recoge argumentos y llama al proceso.
def main(argv: Sequence[str] | None = None) -> int:
    """Punto de entrada CLI, apto para pruebas al aceptar ``argv``."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("imagen", type=Path, help="Imagen de la cartilla")
    parser.add_argument(
        "--carpeta", type=Path, default=Path("addison_plantilla"),
        help="Directorio que contiene la plantilla y sus coordenadas",
    )
    parser.add_argument(
        "--alinear", action="store_true",
        help="La entrada es una fotografía original sin alinear",
    )
    parser.add_argument(
        "--refinar-ecc", action="store_true",
        help="Corrige pequeñas desviaciones tras la alineación",
    )
    parser.add_argument(
        "--sin-rescate-tenues", action="store_true",
        help="Desactiva la comprobación de marcas tenues con plantilla",
    )
    parser.add_argument(
        "--salida", type=Path,
        help="Prefijo para los archivos .csv, .json y _revision.jpg",
    )
    parser.add_argument(
        "--alineacion-local", action="store_true",
        help="Experimental: recuperar deformaciones locales solo tras fallar ORB/SIFT, marcadores y ECC; exige revision manual",
    )
    parser.add_argument(
        "--comparar-cluster", action="store_true",
        help="Añade K-Means, Fuzzy C-Means y DBSCAN experimentales sin modificar respuestas",
    )
    parser.add_argument(
        "--recuperacion-especial", action="store_true",
        help="Comparar varias fotografías de una misma cartilla. No cambia lecturas oficiales; genera propuestas para revisión humana.",
    )
    parser.add_argument("imagenes_adicionales", nargs="*", type=Path,
                        help="Fotografías adicionales (solo con --recuperacion-especial)")
    argumentos = parser.parse_args(argv)
    if argumentos.recuperacion_especial:
        from .comparar_varias_fotos_cartilla import analizar_lote
        destino = argumentos.salida or Path("salida_recuperacion")
        reporte = analizar_lote([argumentos.imagen, *argumentos.imagenes_adicionales],
                               argumentos.carpeta, destino)
        print("Resultados individuales:", len(reporte["resumen"]))
        print("Grupos probables:", len(reporte["agrupaciones_probables"]))
        print("Propuestas para revisión:", len(reporte["sugerencias_pendientes_confirmacion"]))
        print("Archivos:", destino)
        return 0 if not reporte["rechazadas"] else 2
    if argumentos.imagenes_adicionales:
        parser.error("Las imágenes adicionales requieren --recuperacion-especial")
    resultado = procesar(
        argumentos.imagen,
        argumentos.carpeta,
        salida=argumentos.salida,
        alineacion=argumentos.alinear,
        refinar=argumentos.refinar_ecc,
        rescatar_tenues=not argumentos.sin_rescate_tenues,
        comparar_clusters=argumentos.comparar_cluster,
        alineacion_local=argumentos.alineacion_local,
    )
    if resultado.get("exito", True) is False:
        print("ERROR:", resultado["error"])
        return 2

    print("ADDISON v0.5.4:", resultado["resumen"])
    print("Estrategia:", resultado["estrategia"]["tratamientos_aceptacion"])
    print("DNI (no publicar sin validacion):", resultado["dni"])
    return 0

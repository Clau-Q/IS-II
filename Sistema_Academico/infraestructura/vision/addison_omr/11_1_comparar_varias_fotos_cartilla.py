"""ETAPA 11.1 — Comparación CONSERVADORA de varias capturas de una misma cartilla.

Modo expresamente solicitado. No altera decisiones OMR ni calibra confianzas.
Las fotos de una misma hoja pueden ser dependientes (recortes/giro), y el
acuerdo entre tratamientos de una misma imagen tampoco es independencia.

Se agrupan solo lecturas con coincidencia fuerte de DNI parcial y respuestas.
Cada propuesta requiere verificación humana antes de calificar.
"""
from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
import csv
import json

from .ejecutar_flujo_lectura import procesar


def _respuesta_misma_hoja(a: dict, b: dict) -> dict:
    """Criterio conservador: DNI parcial + coincidencia de respuestas válidas."""
    da, db = a['dni'], b['dni']
    posiciones = [(x, y) for x, y in zip(da, db) if x.isdigit() and y.isdigit()]
    coincidencia_dni = sum(x == y for x, y in posiciones)
    dif_dni = len(posiciones) - coincidencia_dni
    aa = a['controles']['area']
    ab = b['controles']['area']
    area_compatible = not (aa['estado'] == ab['estado'] == 'VALIDA'
                           and aa['respuesta'] != ab['respuesta'])
    parejas = [(x['respuesta'], y['respuesta'])
              for x, y in zip(a['respuestas'], b['respuestas'])
              if x['estado'] == y['estado'] == 'VALIDA']
    total_validas = len(parejas)
    iguales = sum(x == y for x, y in parejas)
    compatible = (dif_dni == 0 and coincidencia_dni >= 5 and
                  area_compatible and total_validas >= 60 and
                  iguales / total_validas >= .98)
    return dict(compatible=compatible, digitos_dni_comparados=len(posiciones),
                digitos_dni_iguales=coincidencia_dni,
                respuestas_validas_comparadas=total_validas,
                respuestas_validas_coincidentes=iguales,
                area_compatible=area_compatible)


def _grupos_compatibles(resultados: list[dict]) -> tuple[list[list[int]], list[dict]]:
    """Agrupación completa: todos los pares del grupo deben ser compatibles."""
    pares = {}
    comparaciones = []
    for i in range(len(resultados)):
        for j in range(i + 1, len(resultados)):
            c = _respuesta_misma_hoja(resultados[i], resultados[j])
            pares[i, j] = c['compatible']
            comparaciones.append(dict(imagen_a=resultados[i]['imagen_fuente'],
                                      imagen_b=resultados[j]['imagen_fuente'], **c))
    grupos = []
    for indice in range(len(resultados)):
        asignado = False
        for grupo in grupos:
            if all(pares[min(indice, j), max(indice, j)] for j in grupo):
                grupo.append(indice)
                asignado = True
                break
        if not asignado:
            grupos.append([indice])
    return grupos, comparaciones


def _evaluar_campos(registros: list[dict], campo: str, indice: int | str,
                    archivos: list[str]) -> list[dict]:
    """Sugerencias para registros DUDOSA/SIN_RESPUESTA, nunca cambios oficiales."""
    if campo == 'pregunta':
        items = [r['respuestas'][int(indice) - 1] for r in registros]
    elif campo == 'dni':
        items = [r['detalle_dni'][int(indice) - 1] for r in registros]
    else:
        items = [r['controles'][str(indice)] for r in registros]
    fuertes = [(a, item['respuesta']) for a, item in zip(archivos, items)
               if item['estado'] == 'VALIDA' and item['respuesta'] is not None]
    alternativas = {respuesta for _, respuesta in fuertes}
    if len(alternativas) != 1:
        return []
    candidata = next(iter(alternativas))
    propuestas = []
    for archivo, item in zip(archivos, items):
        if item['estado'] == 'VALIDA':
            continue
        # Nunca ignorar una doble marca. Para una duda, exigir que la candidata
        # esté entre las alternativas detectadas; vacío necesita revisión visual.
        if item['estado'] == 'DOBLE_MARCA':
            continue
        candidatas = item.get('candidatas') or []
        if item['estado'] == 'DUDOSA' and (not candidatas or candidata not in candidatas):
            continue
        if item['estado'] == 'DUDOSA' and any(op != candidata for op in candidatas):
            continue
        coherentes = all(x['estado'] != 'DUDOSA' or
                         not x.get('candidatas') or
                         candidata in x['candidatas'] for x in items)
        if not coherentes:
            continue
        propuestas.append({
            'imagen': archivo, 'campo': campo, 'indice': indice,
            'estado_original': item['estado'],
            'candidatas_originales': candidatas,
            'respuesta_sugerida': candidata,
            'imagenes_con_respuesta_valida': [nombre for nombre, _ in fuertes],
            'confirmacion_manual_obligatoria': True,
            'observacion': ('Marca dudosa coherente con otra captura' if item['estado'] == 'DUDOSA'
                            else 'No detectada en esta captura; revisar visualmente'),
        })
    return propuestas


def analizar_lote(imagenes: Sequence[str | Path], carpeta: str | Path,
                  salida: str | Path) -> dict:
    """Procesa capturas y guarda comparaciones sin modificar el resultado individual.

    Las imágenes con error se registran como rechazadas y no participan en
    propuestas. Las sugerencias NO rellenan datos ni otorgan % de confianza.
    """
    imagenes = [Path(x) for x in imagenes]
    if not imagenes:
        raise ValueError('Se necesita al menos una fotografía')
    if len({str(x.resolve()) for x in imagenes}) != len(imagenes):
        raise ValueError('Hay rutas duplicadas en el lote')
    salida = Path(salida)
    salida.mkdir(parents=True, exist_ok=True)
    resultados, rechazadas = [], []
    resumen = []
    for n, imagen in enumerate(imagenes, 1):
        prefijo = salida / 'individual' / f'{n:02d}_{imagen.stem}'
        try:
            r = procesar(imagen, carpeta, salida=prefijo,
                         alineacion=True, alineacion_local=True)
            if r.get('exito', True) is False:
                rechazadas.append({'imagen': imagen.name, 'error': r['error']})
                resumen.append({'archivo': imagen.name, 'resultado': 'RECHAZADA',
                                'dni': '', 'area': '', 'validas': '', 'dudosas': '',
                                'dobles': '', 'sin_respuesta': '', 'requiere_revision': True})
                continue
            resultados.append(r)
            s = r['resumen']
            resumen.append({'archivo': imagen.name, 'resultado': 'LEIDA',
                            'dni': r['dni'], 'area': r['controles']['area']['respuesta'] or '',
                            'validas': s['VALIDA'], 'dudosas': s['DUDOSA'],
                            'dobles': s['DOBLE_MARCA'], 'sin_respuesta': s['SIN_RESPUESTA'],
                            'requiere_revision': s['requiere_revision']})
        except Exception as error:
            rechazadas.append({'imagen': imagen.name, 'error': str(error)})
            resumen.append({'archivo': imagen.name, 'resultado': 'ERROR',
                            'dni': '', 'area': '', 'validas': '', 'dudosas': '',
                            'dobles': '', 'sin_respuesta': '', 'requiere_revision': True})
    grupos, comparaciones = _grupos_compatibles(resultados)
    agrupaciones = []
    sugerencias = []
    for i, indices in enumerate(grupos, 1):
        registros = [resultados[j] for j in indices]
        archivos = [x['imagen_fuente'] for x in registros]
        agrupaciones.append({'grupo': i, 'imagenes': archivos, 'mismo_original_confirmado': False,
                             'advertencia': 'Solo grupo probable; verificar que sea la misma hoja física'})
        if len(indices) < 2:
            continue
        for pregunta in range(1, 91):
            sugerencias.extend(_evaluar_campos(registros, 'pregunta', pregunta, archivos))
        for columna in range(1, 9):
            sugerencias.extend(_evaluar_campos(registros, 'dni', columna, archivos))
        for area in ('turno', 'area', 'tema'):
            sugerencias.extend(_evaluar_campos(registros, 'control', area, archivos))
    salida_reporte = {
        'modo': 'recuperacion_especial_multifoto',
        'advertencia': ('Los resultados OMR originales no se alteran. Todas las propuestas '
                        'requieren comprobación humana y mismo original físico confirmado. '
                        'Las categorias alta/media/baja NO son porcentajes de acierto.'),
        'agrupaciones_probables': agrupaciones,
        'comparaciones': comparaciones,
        'sugerencias_pendientes_confirmacion': sugerencias,
        'rechazadas': rechazadas,
        'resumen': resumen,
    }
    (salida / 'reporte_recuperacion.json').write_text(
        json.dumps(salida_reporte, ensure_ascii=False, indent=2), encoding='utf-8')
    with (salida / 'resumen.csv').open('w', newline='', encoding='utf-8-sig') as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=list(resumen[0]))
        escritor.writeheader(); escritor.writerows(resumen)
    with (salida / 'sugerencias_revision.csv').open('w', newline='', encoding='utf-8-sig') as archivo:
        columnas = ['imagen', 'campo', 'indice', 'estado_original', 'candidatas_originales',
                    'respuesta_sugerida', 'imagenes_con_respuesta_valida',
                    'confirmacion_manual_obligatoria', 'observacion']
        escritor = csv.DictWriter(archivo, fieldnames=columnas)
        escritor.writeheader()
        for s in sugerencias:
            escritor.writerow({**s,
                'candidatas_originales': '/'.join(s['candidatas_originales']),
                'imagenes_con_respuesta_valida': ' / '.join(s['imagenes_con_respuesta_valida'])})
    return salida_reporte

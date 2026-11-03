"""Comparador EXPLORATORIO de K-Means, Fuzzy C-Means y DBSCAN.

No modifica las decisiones OMR. Los tres métodos usan mediciones de la
MISMA fotografía: NO son pruebas independientes ni probabilidades de acierto.
DBSCAN identifica densidad y puntos atípicos, no marcas verdaderas.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any
import numpy as np
import cv2


# PASO 6.6 — Obtiene características físicas de cada burbuja ya auditada.
def extraer_caracteristicas(
    respuestas: Sequence[Mapping[str, Any]],
) -> tuple[np.ndarray, list[tuple[int, str]], list[float]]:
    """Cuatro señales con escalas *fijas* para no borrar marcas débiles.

    Columnas: oscuridad, contraste local, delta oscuridad contra plantilla,
    delta contraste contra plantilla. Ninguna requiere conocer las respuestas.
    """
    filas: list[list[float]] = []
    etiquetas: list[tuple[int, str]] = []
    fuerza: list[float] = []
    for item in respuestas:
        if not item.get('evidencia_plantilla'):
            raise ValueError('El reporte requiere evidencia_plantilla por pregunta')
        for opcion, ev in item['evidencia_plantilla'].items():
            fraccion = float(ev['fraccion_oscura'])
            contraste = float(ev['contraste_local'])
            df = float(ev['incremento_fraccion_oscura'])
            dc = float(ev['incremento_contraste'])
            if not all(np.isfinite((fraccion, contraste, df, dc))):
                raise ValueError('Mediciones no finitas en el reporte')
            # Escala física legible; no escalar con el mínimo/máximo de la foto.
            filas.append([
                float(np.clip(fraccion, 0, 1)),
                float(np.clip(contraste / 160, -1, 2)),
                float(np.clip(df / .65, -1.5, 1.5)),
                float(np.clip(dc / 150, -1.5, 1.5)),
            ])
            etiquetas.append((int(item['pregunta']), str(opcion)))
            fuerza.append(float(max(0, df) + max(0, dc) / 150))
    if len(filas) < 10:
        raise ValueError('Se necesitan al menos diez burbujas para agrupar')
    return np.asarray(filas, dtype=np.float64), etiquetas, fuerza


# PASO 6.7 — Separa dos grupos por K-Means sin validar respuestas.
def agrupar_kmeans(x: np.ndarray) -> dict[str, Any]:
    cv2.setRNGSeed(2022)
    _, etiquetas, centros = cv2.kmeans(
        x.astype(np.float32), 2, None,
        (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_MAX_ITER, 100, 1e-5),
        15, cv2.KMEANS_PP_CENTERS,
    )
    c = centros.astype(np.float64)
    # Centro más oscuro y con mayor delta se toma como grupo hipotético marcado.
    pesos = np.array([.35, .10, .30, .25])
    oscuro = int(np.argmax(c @ pesos))
    separacion = float(np.linalg.norm(c[0] - c[1]))
    return {'etiquetas': etiquetas.flatten().astype(int).tolist(),
            'centros': np.round(c, 5).tolist(), 'cluster_oscuro': oscuro,
            'separacion': round(separacion, 5)}


# PASO 6.8 — Calcula pertenencia difusa a dos grupos (Fuzzy C-Means).
def agrupar_fuzzy_cmeans(
    x: np.ndarray, *, m: float = 2.0, tolerancia: float = 1e-6,
    max_iter: int = 250,
) -> dict[str, Any]:
    if m <= 1:
        raise ValueError('La fuzzificación m debe ser mayor que 1')
    # Inicialización determinista a partir de cuantiles de una señal conjunta.
    pesos = np.array([.35, .10, .30, .25])
    niveles = x @ pesos
    centros = x[np.argsort(niveles)[[len(x)//10, 9*len(x)//10]]].copy()
    membresia = np.full((len(x), 2), .5, dtype=np.float64)
    iteraciones = 0
    for it in range(max_iter):
        d = np.maximum(np.linalg.norm(x[:, None, :] - centros[None, :, :], axis=2), 1e-10)
        potencias = (d ** (-2.0 / (m - 1)))
        nueva = potencias / potencias.sum(axis=1, keepdims=True)
        um = nueva ** m
        nuevos_centros = (um.T @ x) / um.sum(axis=0)[:, None]
        iteraciones = it + 1
        cambio = float(np.max(np.abs(nueva - membresia)))
        membresia = nueva
        centros = nuevos_centros
        if cambio < tolerancia:
            break
    oscuro = int(np.argmax(centros @ pesos))
    return {'pertenencias_oscuras': np.round(membresia[:, oscuro], 5).tolist(),
            'centros': np.round(centros, 5).tolist(), 'cluster_oscuro': oscuro,
            'separacion': round(float(np.linalg.norm(centros[0] - centros[1])), 5),
            'iteraciones': iteraciones,
            'advertencia': 'Las pertenencias difusas no son probabilidades de acierto'}


# PASO 6.9 — Agrupa por densidad e identifica atípicos sin etiquetas OMR.
def agrupar_dbscan(
    x: np.ndarray, *, eps: float = .18, min_muestras: int = 5
) -> dict[str, Any]:
    if eps <= 0 or min_muestras < 2:
        raise ValueError('eps debe ser positivo y min_muestras >= 2')
    # Sin scikit-learn: implementación determinista para ~450 burbujas/hoja.
    distancias2 = np.sum((x[:, None, :] - x[None, :, :]) ** 2, axis=2)
    vecinos = [np.flatnonzero(distancias2[i] <= eps**2).tolist() for i in range(len(x))]
    # -2: no visitado; -1: ruido, >=0: índice de cluster.
    etiquetas = np.full(len(x), -2, dtype=int)
    cluster = 0
    nucleos = [len(v) >= min_muestras for v in vecinos]
    for i in range(len(x)):
        if etiquetas[i] != -2:
            continue
        if not nucleos[i]:
            etiquetas[i] = -1
            continue
        etiquetas[i] = cluster
        cola = [i]
        indice = 0
        while indice < len(cola):
            actual = cola[indice]
            indice += 1
            if not nucleos[actual]:
                continue
            for j in vecinos[actual]:
                if etiquetas[j] == -1:
                    etiquetas[j] = cluster
                if etiquetas[j] != -2:
                    continue
                etiquetas[j] = cluster
                cola.append(j)
        cluster += 1
    return {'etiquetas': etiquetas.tolist(), 'grupos': cluster,
            'atipicos': int(np.sum(etiquetas == -1)),
            'eps': eps, 'min_muestras': min_muestras,
            'advertencia': 'Atípico DBSCAN NO significa respuesta marcada o inválida'}


# PASO 6.10 — Comprueba evidencia física mínima para una propuesta experimental.
def _evidencia_minima(e: Mapping[str, Any]) -> bool:
    fr = float(e['fraccion_oscura'])
    dc = float(e['incremento_contraste'])
    df = float(e['incremento_fraccion_oscura'])
    # Guardas ilustrativas. Deben calibrarse con verdad terreno; no son regla oficial.
    return (fr >= .60 and dc >= 14 and df >= .11) or (
        fr >= .86 and dc >= 26 and df >= .06
    )


# PASO 6.11 — Compara propuestas por pregunta SIN alterar la decisión oficial.
def comparar_agrupamientos(
    resultado: Mapping[str, Any],
    *, eps_dbscan: float = .18, min_muestras: int = 5,
) -> dict[str, Any]:
    """Diagnóstico reproducible para cada pregunta, incluso si es DUDOSA.

    El acuerdo K-Means/FCM NO autoriza a sustituir el estado del lector. Un
    falso positivo puede existir en ambos por compartir las mismas mediciones.
    """
    respuestas = resultado['respuestas']
    x, posiciones, _ = extraer_caracteristicas(respuestas)
    km = agrupar_kmeans(x)
    fc = agrupar_fuzzy_cmeans(x)
    db = agrupar_dbscan(x, eps=eps_dbscan, min_muestras=min_muestras)
    centro_k = np.asarray(km['centros'][km['cluster_oscuro']])
    centro_f = np.asarray(fc['centros'][fc['cluster_oscuro']])
    # Las agrupaciones claras/vacías pueden generar grupos 'oscuros' artificiales.
    fiable_k = bool(km['separacion'] >= .35 and (centro_k[0] >= .62 or centro_k[2] >= .25))
    fiable_f = bool(fc['separacion'] >= .35 and (centro_f[0] >= .62 or centro_f[2] >= .25))
    por_pregunta: dict[int, dict[str, Any]] = {
        int(r['pregunta']): {'pregunta': int(r['pregunta']),
            'estado_actual': r['estado'], 'respuesta_actual': r.get('respuesta'),
            'candidatas_actuales': list(r.get('candidatas', [])),
            'opciones': {}, 'kmeans': [], 'fuzzy_cmeans': [], 'atipicas_dbscan': []}
        for r in respuestas
    }
    for i, (numero, opcion) in enumerate(posiciones):
        pregunta = por_pregunta[numero]
        ev = next(r for r in respuestas if int(r['pregunta']) == numero)['evidencia_plantilla'][opcion]
        guarda = _evidencia_minima(ev)
        voto_k = bool(fiable_k and guarda and km['etiquetas'][i] == km['cluster_oscuro'])
        pertenencia = float(fc['pertenencias_oscuras'][i])
        voto_f = bool(fiable_f and guarda and pertenencia >= .70)
        ruido = db['etiquetas'][i] == -1
        pregunta['opciones'][opcion] = {
            'fraccion_oscura': ev['fraccion_oscura'],
            'delta_fraccion': ev['incremento_fraccion_oscura'],
            'delta_contraste': ev['incremento_contraste'],
            'kmeans_marca_hipotetica': voto_k,
            'fuzzy_pertenencia_grupo_oscuro': pertenencia,
            'fuzzy_marca_hipotetica': voto_f,
            'dbscan_cluster': int(db['etiquetas'][i]),
            'dbscan_atipica': ruido,
            'supera_guarda_fisica': guarda,
        }
        if voto_k:
            pregunta['kmeans'].append(opcion)
        if voto_f:
            pregunta['fuzzy_cmeans'].append(opcion)
        if ruido:
            pregunta['atipicas_dbscan'].append(opcion)
    vacia = bool(resultado.get('resumen', {}).get('hoja_vacia_probable', False))
    resueltas = 0
    compatibles = 0
    observaciones = []
    for pregunta in por_pregunta.values():
        a = set(pregunta['kmeans'])
        b = set(pregunta['fuzzy_cmeans'])
        if vacia:
            propuesta, alternativa = 'SIN_EVIDENCIA', None
        elif a == b and len(a) == 1:
            propuesta, alternativa = 'UNICA_COINCIDENTE', next(iter(a))
        elif len(a | b) >= 2:
            propuesta, alternativa = 'POSIBLE_DOBLE_O_DESACUERDO', None
        elif a or b:
            propuesta, alternativa = 'DESACUERDO', next(iter(a | b))
        else:
            propuesta, alternativa = 'SIN_EVIDENCIA', None
        pregunta['propuesta_experimental'] = propuesta
        pregunta['alternativa_experimental'] = alternativa
        pregunta['coincide_con_oficial'] = (
            pregunta['estado_actual'] == 'VALIDA'
            and propuesta == 'UNICA_COINCIDENTE'
            and pregunta['respuesta_actual'] == alternativa
        )
        if pregunta['coincide_con_oficial']:
            compatibles += 1
        if pregunta['estado_actual'] == 'DUDOSA' and propuesta == 'UNICA_COINCIDENTE':
            resueltas += 1
            observaciones.append({'pregunta': pregunta['pregunta'],
                                   'alternativa_sugerida': alternativa,
                                   'aviso': 'SOLAMENTE candidata a revisión manual'})
    return {
        'experimental': True,
        'modifica_resultados_oficiales': False,
        'nota': ('Modelos entrenados con burbujas de una sola foto; no equivalen a '
                 'tres comprobaciones independientes ni a precisión demostrada'),
        'configuracion': {'eps_dbscan': eps_dbscan, 'min_muestras': min_muestras,
                          'fuzzy_m': 2.0, 'fuzzy_pertenencia_minima': .70},
        'calidad_grupos': {'kmeans_habilitado': fiable_k,
                           'fuzzy_habilitado': fiable_f,
                           'kmeans_separacion': km['separacion'],
                           'fuzzy_separacion': fc['separacion']},
        'dbscan': {'grupos': db['grupos'], 'burbujas_atipicas': db['atipicos'],
                   'advertencia': db['advertencia']},
        'resumen': {'preguntas': len(por_pregunta),
                   'dudosas_oficiales': sum(r['estado']=='DUDOSA' for r in respuestas),
                   'dudosas_con_candidata_experimental': resueltas,
                   'validas_oficiales_con_candidato_coincidente': compatibles},
        'dudosas_a_revisar': observaciones,
        'preguntas': list(por_pregunta.values()),
    }


# PASO 10.7 — Exporta la comparativa por pregunta a un CSV auditable.
def guardar_comparacion_csv(ruta: str, analisis: Mapping[str, Any]) -> None:
    from pathlib import Path
    import csv
    columnas = ['pregunta', 'estado_actual', 'respuesta_actual', 'kmeans',
                'fuzzy_cmeans', 'atipicas_dbscan', 'propuesta_experimental',
                'alternativa_experimental', 'coincide_con_oficial']
    destino = Path(ruta)
    destino.parent.mkdir(parents=True, exist_ok=True)
    with destino.open('w', newline='', encoding='utf-8-sig') as fd:
        wr = csv.DictWriter(fd, fieldnames=columnas)
        wr.writeheader()
        for p in analisis['preguntas']:
            wr.writerow({k: '/'.join(p[k]) if isinstance(p.get(k), list)
                          else p.get(k, '') for k in columnas})

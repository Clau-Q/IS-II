"""Reglas de puntuación de una cartilla resuelta."""
from decimal import Decimal


def calificar(filas, penalizacion):
    detalles = []
    materias = {}
    correctas = incorrectas = blancos = 0
    for f in filas:
        tipo = f['resolucion'] or ('UNICA' if f['lectura'] else 'BLANCO')
        if tipo == 'MARCA_UNICA':
            tipo = 'UNICA'
        marcada = f['corregida'] if f['resolucion'] else f['lectura']
        correcta = tipo == 'UNICA' and marcada == f['clave']
        puntaje = f['puntaje'] if correcta else (penalizacion if tipo == 'UNICA' else Decimal(0))
        correctas += int(correcta)
        incorrectas += int(tipo == 'UNICA' and not correcta)
        blancos += int(tipo != 'UNICA')
        dato = dict(f, tipo=tipo, marcada=marcada, correcta=correcta, obtenido=puntaje)
        detalles.append(dato)
        materia = materias.setdefault(f['id_materia'], {'total': 0, 'correctas': 0, 'incorrectas': 0, 'blancos': 0, 'puntaje': Decimal(0)})
        materia['total'] += 1
        materia['correctas'] += int(correcta)
        materia['incorrectas'] += int(tipo == 'UNICA' and not correcta)
        materia['blancos'] += int(tipo != 'UNICA')
        materia['puntaje'] += puntaje
    return detalles, materias, correctas, incorrectas, blancos, max(Decimal(0), sum((x['obtenido'] for x in detalles), Decimal(0)))

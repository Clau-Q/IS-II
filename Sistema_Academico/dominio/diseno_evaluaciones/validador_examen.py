"""Reglas para la estructura y distribución de un examen."""
from decimal import Decimal


class ValidadorExamen:
    @staticmethod
    def calcular_distribucion(ids, preguntas, puntajes, puntaje_total):
        por_id = {p['id_version']: p for p in preguntas}
        if len(por_id) != len(ids) or set(por_id) != set(ids):
            raise ValueError('Alguna pregunta ya no está aprobada o no corresponde al área.')
        materias = {p['id_materia'] for p in preguntas}
        if any(m not in puntajes for m in materias):
            raise ValueError('Falta el puntaje por pregunta de alguna materia seleccionada.')
        cantidades = {}
        ejes = {}
        for id_pregunta in ids:
            pregunta = por_id[id_pregunta]
            materia, eje = pregunta['id_materia'], pregunta['id_eje']
            cantidades[materia] = cantidades.get(materia, 0) + 1
            ejes[eje] = ejes.get(eje, Decimal(0)) + puntajes[materia]
        if sum(ejes.values()) != puntaje_total:
            raise ValueError(f'La suma de puntajes debe ser exactamente {puntaje_total}.')
        pesos = {}
        for eje, puntos in ejes.items():
            peso = puntos * 100 / puntaje_total
            if peso.quantize(Decimal('0.000000001')) != peso:
                raise ValueError('Los puntajes producen un peso de eje con más de 9 decimales.')
            pesos[eje] = peso
        return por_id, cantidades, pesos

    @staticmethod
    def validar_clave(respuestas, numeros):
        if set(respuestas) != set(numeros):
            raise ValueError('La clave debe contener exactamente todas las preguntas de la versión.')

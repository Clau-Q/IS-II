"""Casos de uso de configuración de exámenes y claves."""
from decimal import Decimal, InvalidOperation


class DisenoExamenAppService:
    def __init__(self, repositorio):
        self.repositorio = repositorio

    def consultar(self, examen):
        return self.repositorio.consultar(examen)

    def distribucion(self, examen):
        return self.repositorio.distribucion(examen)

    def configurar(self, examen, ids, puntajes, versiones, penalizacion, usuario):
        try:
            preguntas = list(dict.fromkeys(int(x) for x in ids))
            importes = {int(k): Decimal(v) for k, v in puntajes.items()}
            penalizacion = Decimal(penalizacion or '0')
        except (ValueError, InvalidOperation):
            raise ValueError('Revisa los identificadores y puntajes.') from None
        if not preguntas or not versiones or any(v not in ('A', 'B') for v in versiones):
            raise ValueError('Selecciona preguntas y al menos una versión.')
        if not penalizacion.is_finite() or penalizacion > 0 or penalizacion.as_tuple().exponent < -9:
            raise ValueError('La penalización debe ser cero o negativa, con hasta 9 decimales.')
        if any(not v.is_finite() or v <= 0 or v.as_tuple().exponent < -9 for v in importes.values()):
            raise ValueError('Cada puntaje debe ser positivo y tener hasta 9 decimales.')
        self.repositorio.configurar(examen, preguntas, importes, versiones, penalizacion, usuario)

    def crear_clave(self, version, valores, motivo, usuario):
        motivo = (motivo or '').strip()
        if not motivo:
            raise ValueError('Indica el motivo de la nueva revisión de clave.')
        try:
            respuestas = {int(k): str(v).strip().upper() for k, v in valores.items()}
        except ValueError:
            raise ValueError('La numeración no es válida.') from None
        if not respuestas or any(v not in ('A', 'B', 'C', 'D', 'E') for v in respuestas.values()):
            raise ValueError('Cada respuesta debe estar entre A y E.')
        self.repositorio.crear_clave(version, respuestas, motivo, usuario)

"""Reglas de transición de la estructura de un examen."""


class Examen:
    @staticmethod
    def validar_configuracion(estado, tiene_versiones):
        if estado not in ('BORRADOR', 'CONFIGURACION'):
            raise ValueError('El examen no está disponible para configurar.')
        if tiene_versiones:
            raise ValueError('El examen ya tiene versiones; no se reemplazará su configuración.')

    @staticmethod
    def validar_revision_clave(estado, tiene_resultados):
        if estado not in ('APROBADO', 'APLICADO', 'CERRADO'):
            raise ValueError('La versión no pertenece a un examen aprobado.')
        if tiene_resultados:
            raise ValueError('Ya hay resultados vigentes. La corrección de clave requiere recalificación integral.')

    @staticmethod
    def ordenar_versiones(ids, codigo):
        if codigo == 'A':
            return list(ids)
        if codigo == 'B':
            return list(reversed(ids))
        raise ValueError('Código de versión no válido.')

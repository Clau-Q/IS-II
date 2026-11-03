"""Reglas para conservar los periodos de una asignación."""


class AsignacionAcademica:
    @staticmethod
    def requiere_cambio(actual, identificador, fecha):
        if not actual:
            return True
        if actual['valor'] == identificador:
            return False
        if fecha <= actual['fecha_inicio']:
            raise ValueError('La fecha del cambio debe ser posterior al inicio de la asignación actual.')
        return True

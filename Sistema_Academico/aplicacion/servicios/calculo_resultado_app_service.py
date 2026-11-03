"""Coordina el cálculo inicial de los resultados de un examen."""


class CalculoResultadoAppService:
    def __init__(self, repositorio):
        self.repositorio = repositorio

    def calcular_resultados(self, examen_id, usuario_id):
        if not examen_id:
            raise ValueError('Selecciona un examen.')
        return self.repositorio.calcular(examen_id, usuario_id)

"""Casos de uso para la revisión y consulta de resultados."""


class ResultadosAppService:
    def __init__(self, repositorio):
        self.repositorio = repositorio

    def corregir(self, respuesta, resolucion, marca, motivo, usuario):
        motivo = (motivo or '').strip()
        marca = (marca or '').strip().upper()
        if resolucion not in ('MARCA_UNICA', 'BLANCO', 'MULTIPLE_CONFIRMADA'):
            raise ValueError('Selecciona una resolución válida.')
        if resolucion == 'MARCA_UNICA' and marca not in ('A', 'B', 'C', 'D', 'E'):
            raise ValueError('Selecciona una respuesta de A a E.')
        if not motivo:
            raise ValueError('Indica el motivo de la corrección.')
        self.repositorio.corregir(respuesta, resolucion, marca if resolucion == 'MARCA_UNICA' else None, motivo, usuario)

    def examenes(self):
        return self.repositorio.examenes()

    def lecturas(self, examen):
        return self.repositorio.lecturas(examen)

    def historial_lecturas(self, examen):
        return self.repositorio.historial_lecturas(examen)

    def validar_cartilla(self, cartilla):
        return self.repositorio.validar_cartilla(cartilla)

    def imagen_cartilla(self, cartilla):
        return self.repositorio.imagen_cartilla(cartilla)

    def resultados(self, examen):
        return self.repositorio.resultados(examen)

    def detalle_coordinador(self, resultado):
        return self.repositorio.detalle_coordinador(resultado)

    def revisar_resultado(self, resultado, usuario):
        return self.repositorio.revisar_resultado(resultado, usuario)

    def publicar(self, examen, usuario):
        if not examen:
            raise ValueError('Selecciona un examen.')
        return self.repositorio.publicar(examen, usuario)

    def ranking(self, examen):
        return self.repositorio.ranking(examen)

    def mis_resultados(self, usuario):
        return self.repositorio.mis_resultados(usuario)

    def detalle(self, usuario, resultado):
        return self.repositorio.detalle(usuario, resultado)

    def materias(self, usuario, resultado):
        return self.repositorio.materias(usuario, resultado)

    def datos_director(self, ciclo):
        return self.repositorio.datos_director(ciclo)

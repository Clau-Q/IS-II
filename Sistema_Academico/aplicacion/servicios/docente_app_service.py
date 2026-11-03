"""Casos de uso de creación, consulta y revisión de preguntas docentes."""
from dominio.banco_preguntas.contenido_docente import validar_contenido


class DocenteAppService:
    def __init__(self, repositorio):
        self.repositorio = repositorio

    def catalogos(self, usuario):
        return self.repositorio.catalogos(usuario)

    def examenes(self):
        return self.repositorio.examenes()

    def crear_tema(self, usuario, materia, nombre):
        nombre = (nombre or '').strip()
        try:
            materia = int(materia)
        except (TypeError, ValueError):
            raise ValueError('Selecciona una materia válida.') from None
        if not nombre or len(nombre) > 150:
            raise ValueError('El tema debe tener entre 1 y 150 caracteres.')
        self.repositorio.crear_tema(usuario, materia, nombre)

    def preguntas(self, usuario, filtros):
        estado = filtros.get('estado', '')
        if estado not in ('', 'BORRADOR', 'REVISION', 'APROBADA', 'INACTIVA'):
            raise ValueError('Estado no válido.')
        try:
            materia = int(filtros.get('materia') or 0)
            examen = int(filtros.get('examen') or 0)
        except ValueError:
            raise ValueError('Materia no válida.') from None
        return self.repositorio.preguntas(usuario, estado, materia, examen)

    def obtener(self, usuario, pregunta, version=None):
        return self.repositorio.obtener(usuario, pregunta, version)

    def guardar(self, usuario, datos, archivos, pregunta=None):
        enunciado, respuesta, alternativas = validar_contenido(datos)
        if datos.get('accion') not in ('guardar', 'enviar'):
            raise ValueError('Selecciona una acción válida.')
        try:
            version = int(datos.get('version') or 0)
            materia = int(datos.get('materia') or 0)
            tema = int(datos.get('tema') or 0)
            examen = int(datos.get('examen') or 0)
            areas = list(dict.fromkeys(int(valor) for valor in datos.getlist('areas')))
        except (TypeError, ValueError):
            raise ValueError('Selecciona materia, tema y áreas válidos.') from None
        tema_nuevo = (datos.get('tema_nuevo') or '').strip()
        if len(tema_nuevo) > 150:
            raise ValueError('El tema admite hasta 150 caracteres.')
        if not pregunta and (not materia or not (tema or tema_nuevo) or not areas or not examen):
            raise ValueError('Selecciona un examen, materia, tema y al menos un área.')
        return self.repositorio.guardar(usuario, pregunta, version, materia, tema, areas, enunciado, respuesta, alternativas, archivos, datos.get('accion') == 'enviar', examen, tema_nuevo)

    def estadisticas(self, usuario):
        return self.repositorio.estadisticas(usuario)

    def imagen(self, usuario, imagen, coordinador=False):
        return self.repositorio.imagen(usuario, imagen, coordinador)

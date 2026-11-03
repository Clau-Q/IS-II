"""Casos de uso de la organización académica."""
from dominio.organizacion_academica.i_organizacion_repositorio import IOrganizacionRepositorio
from dominio.organizacion_academica.reglas_organizacion import TIPOS, identificador, validar_datos, validar_estado


class OrganizacionAppService:
    def __init__(self, repositorio: IOrganizacionRepositorio):
        self.repositorio = repositorio

    def listar(self):
        return self.repositorio.listar()

    def ejecutar(self, accion, tipo, datos):
        if accion in ('asignar', 'desasignar'):
            docente = identificador(datos.get('docente'), 'un docente')
            materia = identificador(datos.get('materia'), 'una materia')
            return self.repositorio.asignar(docente, materia, accion == 'asignar')
        if tipo not in TIPOS:
            raise ValueError('Tipo de elemento no válido.')
        if accion in ('crear', 'editar'):
            valores = validar_datos(tipo, datos)
            if accion == 'crear':
                return self.repositorio.crear(tipo, valores)
            elemento = identificador(datos.get('id'), 'un elemento')
            return self.repositorio.actualizar(tipo, elemento, valores)
        if accion == 'estado':
            elemento = identificador(datos.get('id'), 'un elemento')
            estado = validar_estado(tipo, datos.get('estado'))
            return self.repositorio.estado(tipo, elemento, estado)
        raise ValueError('Acción no válida.')

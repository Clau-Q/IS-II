from dominio.identidad_acceso.autorizacion import Autorizacion
from dominio.identidad_acceso.i_gestion_usuarios_repositorio import IGestionUsuariosRepositorio


class GestionUsuariosAppService:
    def __init__(self, repositorio: IGestionUsuariosRepositorio, protector):
        self.repositorio = repositorio
        self.protector = protector

    def crear(self, formulario, director):
        datos = {campo: formulario.get(campo, "").strip() for campo in ("username", "nombres", "apellidos")}
        roles = formulario.get("roles", [])
        clave = formulario.get("contrasena", "")
        if not all(datos.values()) or len(clave) < 8 or not roles:
            raise ValueError("Complete usuario, nombres y apellidos, seleccione roles y use una contraseña de al menos 8 caracteres.")
        Autorizacion.validar_roles(roles, director)
        self.repositorio.crear(datos, self.protector.generar_hash(clave), roles)

    def cambiar_estado(self, id_usuario, estado, director):
        if estado not in ("ACTIVO", "INACTIVO"):
            raise ValueError("Estado no válido.")
        self.repositorio.estado(id_usuario, estado, director)

    def listar(self):
        return self.repositorio.listar()

    def cambiar_roles(self, id_usuario, roles, director, actor):
        Autorizacion.validar_roles(roles, director)
        self.repositorio.cambiar_roles(id_usuario, roles, director, actor)

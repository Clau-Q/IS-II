class GestionUsuariosAppService:
    def __init__(self, repositorio, protector):
        self.repositorio = repositorio
        self.protector = protector

    def crear(self, formulario, director):
        datos = {campo: formulario.get(campo, "").strip() for campo in ("username", "nombres", "apellidos")}
        roles = formulario.getlist("roles")
        clave = formulario.get("contrasena", "")
        if not all(datos.values()) or len(clave) < 8 or not roles:
            raise ValueError("Complete usuario, nombres y apellidos, seleccione roles y use una contraseña de al menos 8 caracteres.")
        if any(r not in ("ESTUDIANTE", "DOCENTE", "COORDINADOR", "DIRECTOR") for r in roles) or len(set(roles)) != len(roles):
            raise ValueError("Roles no válidos.")
        if "ESTUDIANTE" in roles and len(roles) != 1:
            raise ValueError("El rol estudiante no se puede combinar con otros roles.")
        if "DIRECTOR" in roles and not director:
            raise PermissionError("Solo un director puede asignar el rol director.")
        self.repositorio.crear(datos, self.protector.generar_hash(clave), roles)

    def cambiar_estado(self, id_usuario, estado, director):
        if estado not in ("ACTIVO", "INACTIVO"):
            raise ValueError("Estado no válido.")
        self.repositorio.estado(id_usuario, estado, director)

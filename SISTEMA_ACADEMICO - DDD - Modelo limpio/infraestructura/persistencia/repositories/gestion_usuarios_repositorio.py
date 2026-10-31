from sqlalchemy import text


class GestionUsuariosRepositorio:
    def __init__(self, motor):
        self.motor = motor

    def listar(self):
        with self.motor.connect() as c:
            return c.execute(text("SELECT u.id_usuario,u.username,u.nombres,u.apellidos,u.estado,GROUP_CONCAT(r.nombre ORDER BY r.nombre SEPARATOR ', ') AS roles FROM usuarios u LEFT JOIN usuario_roles ur ON ur.id_usuario=u.id_usuario LEFT JOIN roles r ON r.id_rol=ur.id_rol GROUP BY u.id_usuario,u.username,u.nombres,u.apellidos,u.estado ORDER BY u.username")).mappings().all()

    def crear(self, datos, hash_clave, roles):
        with self.motor.begin() as c:
            resultado = c.execute(text("INSERT INTO usuarios(username,password_hash,nombres,apellidos,estado) VALUES (:username,:clave,:nombres,:apellidos,'ACTIVO')"), {**datos, "clave": hash_clave})
            id_usuario = resultado.lastrowid
            for rol in roles:
                c.execute(text("INSERT INTO usuario_roles(id_usuario,id_rol) SELECT :id,id_rol FROM roles WHERE nombre=:rol"), {"id": id_usuario, "rol": rol})
            if "DOCENTE" in roles:
                c.execute(text("INSERT INTO docentes(id_usuario) VALUES (:id)"), {"id": id_usuario})
            if "COORDINADOR" in roles:
                c.execute(text("INSERT INTO coordinadores(id_usuario) VALUES (:id)"), {"id": id_usuario})
            if "DIRECTOR" in roles:
                c.execute(text("INSERT INTO directores(id_usuario) VALUES (:id)"), {"id": id_usuario})

    def estado(self, id_usuario, estado, director):
        with self.motor.begin() as c:
            cuenta = c.execute(text("SELECT u.username, EXISTS(SELECT 1 FROM usuario_roles ur JOIN roles r ON r.id_rol=ur.id_rol WHERE ur.id_usuario=u.id_usuario AND r.nombre='DIRECTOR') AS es_director FROM usuarios u WHERE u.id_usuario=:id FOR UPDATE"), {"id": id_usuario}).mappings().first()
            if not cuenta:
                raise ValueError("La cuenta no existe.")
            if cuenta["es_director"] and not director:
                raise PermissionError("Solo un director puede modificar cuentas de director.")
            c.execute(text("UPDATE usuarios SET estado=:estado WHERE id_usuario=:id"), {"id": id_usuario, "estado": estado})

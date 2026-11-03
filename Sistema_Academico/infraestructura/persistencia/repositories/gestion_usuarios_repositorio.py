from sqlalchemy import text
from dominio.identidad_acceso.autorizacion import Autorizacion


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
            Autorizacion.validar_modificacion_cuenta(cuenta["es_director"], director)
            c.execute(text("UPDATE usuarios SET estado=:estado WHERE id_usuario=:id"), {"id": id_usuario, "estado": estado})

    def cambiar_roles(self, id_usuario, roles, director, actor):
        with self.motor.begin() as c:
            cuenta = c.execute(text("SELECT id_usuario,EXISTS(SELECT 1 FROM usuario_roles ur JOIN roles r ON r.id_rol=ur.id_rol WHERE ur.id_usuario=usuarios.id_usuario AND r.nombre='DIRECTOR') AS es_director FROM usuarios WHERE id_usuario=:id FOR UPDATE"), {'id': id_usuario}).mappings().first()
            if not cuenta:
                raise ValueError('La cuenta no existe.')
            Autorizacion.validar_modificacion_cuenta(cuenta['es_director'], director)
            if id_usuario == actor:
                raise ValueError('No puedes cambiar los roles de tu propia cuenta.')
            vinculado = c.execute(text('SELECT COUNT(*) FROM estudiantes WHERE id_usuario=:id'), {'id': id_usuario}).scalar_one()
            if vinculado and roles != ['ESTUDIANTE']:
                raise ValueError('Esta cuenta está vinculada a un estudiante y debe conservar su rol.')
            c.execute(text('DELETE FROM usuario_roles WHERE id_usuario=:id'), {'id': id_usuario})
            for rol in roles:
                c.execute(text('INSERT INTO usuario_roles(id_usuario,id_rol) SELECT :id,id_rol FROM roles WHERE nombre=:rol'), {'id': id_usuario,'rol': rol})
            for rol, tabla in (('DOCENTE','docentes'), ('COORDINADOR','coordinadores'), ('DIRECTOR','directores')):
                if rol in roles:
                    c.execute(text(f'INSERT INTO {tabla}(id_usuario) SELECT :id WHERE NOT EXISTS (SELECT 1 FROM {tabla} WHERE id_usuario=:id)'), {'id': id_usuario})

#!/usr/bin/python
# -*- coding: utf-8 -*-

from dominio.identidad_acceso.i_cuenta_repositorio import ICuentaRepositorio
from sqlalchemy import text


class CuentaUsuarioORMRepositorio(ICuentaRepositorio):

    def guardar(self, cuenta_usuario):
        pass

    def buscar_por_id(self, id):
        pass

    def listar(self, filtros):
        pass

    def buscar_por_nombre(self, nombre):
        with self.session.connect() as conexion:
            usuario = conexion.execute(text("SELECT id_usuario, username, password_hash, nombres, estado FROM usuarios WHERE username = :nombre"), {"nombre": nombre}).mappings().first()
            if usuario is None:
                return None
            roles = conexion.execute(text("SELECT r.nombre FROM roles r JOIN usuario_roles ur ON ur.id_rol = r.id_rol WHERE ur.id_usuario = :id"), {"id": usuario["id_usuario"]}).scalars().all()
        return {"id": usuario["id_usuario"], "usuario": usuario["username"], "nombre": usuario["nombres"], "password_hash": usuario["password_hash"], "activa": usuario["estado"] == "ACTIVO", "roles": list(roles)}

    def __init__(self, session):
        self.session = session

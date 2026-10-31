#!/usr/bin/python
# -*- coding: utf-8 -*-

from dominio.organizacion_academica.i_estudiante_repositorio import IEstudianteRepositorio
from sqlalchemy import text


class EstudianteORMRepositorio(IEstudianteRepositorio):

    def guardar(self, estudiante):
        with self.session.begin() as conexion:
            conexion.execute(text("INSERT INTO estudiantes (codigo_estudiante, nombres, apellidos, dni, email, telefono) VALUES (:codigo, :nombres, :apellidos, :dni, :email, :telefono)"), estudiante)

    def buscar_por_id(self, id):
        with self.session.connect() as conexion:
            return conexion.execute(text("SELECT * FROM estudiantes WHERE id_estudiante=:id"), {"id": id}).mappings().first()

    def listar(self, filtros):
        with self.session.connect() as conexion:
            return conexion.execute(text("SELECT id_estudiante, codigo_estudiante, nombres, apellidos, dni, email, telefono, estado, id_usuario FROM estudiantes WHERE codigo_estudiante LIKE :q OR nombres LIKE :q OR apellidos LIKE :q ORDER BY apellidos, nombres LIMIT 200"), {"q": "%" + filtros.get("busqueda", "") + "%"}).mappings().all()

    def actualizar(self, id, datos):
        with self.session.begin() as conexion:
            return conexion.execute(text("UPDATE estudiantes SET codigo_estudiante=:codigo, nombres=:nombres, apellidos=:apellidos, dni=:dni, email=:email, telefono=:telefono WHERE id_estudiante=:id"), {**datos, "id": id}).rowcount

    def cambiar_estado(self, id, estado):
        with self.session.begin() as conexion:
            return conexion.execute(text("UPDATE estudiantes SET estado=:estado WHERE id_estudiante=:id"), {"id": id, "estado": estado}).rowcount

    def vincular_cuenta(self, id, nombre):
        with self.session.begin() as conexion:
            cuenta = conexion.execute(text("SELECT u.id_usuario FROM usuarios u JOIN usuario_roles ur ON ur.id_usuario=u.id_usuario JOIN roles r ON r.id_rol=ur.id_rol WHERE u.username=:nombre AND u.estado='ACTIVO' AND r.nombre='ESTUDIANTE' FOR UPDATE"), {"nombre": nombre}).scalar_one_or_none()
            if cuenta is None:
                raise ValueError("No existe una cuenta activa con rol estudiante para ese usuario.")
            estudiante = conexion.execute(text("SELECT id_usuario FROM estudiantes WHERE id_estudiante=:id FOR UPDATE"), {"id": id}).mappings().first()
            if estudiante is None:
                raise ValueError("El estudiante no existe.")
            if estudiante["id_usuario"] is not None:
                raise ValueError("El estudiante ya tiene una cuenta vinculada.")
            conexion.execute(text("UPDATE estudiantes SET id_usuario=:cuenta WHERE id_estudiante=:id"), {"cuenta": cuenta, "id": id})

    def __init__(self, session):
        self.session = session

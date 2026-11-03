#!/usr/bin/python
# -*- coding: utf-8 -*-

from dominio.organizacion_academica.i_estudiante_repositorio import IEstudianteRepositorio
from dominio.organizacion_academica.asignacion_academica import AsignacionAcademica
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

    def consultar_asignaciones(self, id):
        with self.session.connect() as c:
            areas = c.execute(text("SELECT h.fecha_inicio,h.fecha_fin,a.nombre FROM estudiante_area_historial h JOIN areas a ON a.id_area=h.id_area WHERE h.id_estudiante=:id ORDER BY h.fecha_inicio DESC"), {"id": id}).mappings().all()
            grupos = c.execute(text("SELECT h.fecha_inicio,h.fecha_fin,g.nombre FROM estudiante_grupo_historial h JOIN grupos_academicos g ON g.id_grupo=h.id_grupo WHERE h.id_estudiante=:id ORDER BY h.fecha_inicio DESC"), {"id": id}).mappings().all()
            opciones_areas = c.execute(text("SELECT id_area AS id,nombre FROM areas WHERE estado='ACTIVO' ORDER BY nombre")).mappings().all()
            opciones_grupos = c.execute(text("SELECT g.id_grupo AS id,CONCAT(g.nombre,' · ',c.nombre) AS nombre FROM grupos_academicos g JOIN ciclos_preparacion c ON c.id_ciclo=g.id_ciclo WHERE g.estado='ACTIVO' AND c.estado='ACTIVO' ORDER BY g.nombre")).mappings().all()
            return areas, grupos, opciones_areas, opciones_grupos

    def cambiar_asignacion(self, id, grupo, area, fecha):
        with self.session.begin() as c:
            estudiante = c.execute(text("SELECT estado FROM estudiantes WHERE id_estudiante=:id FOR UPDATE"), {"id": id}).scalar_one_or_none()
            if estudiante != 'ACTIVO':
                raise ValueError('El estudiante no existe o está inactivo.')
            if not c.execute(text("SELECT id_area FROM areas WHERE id_area=:id AND estado='ACTIVO' FOR UPDATE"), {"id": area}).scalar_one_or_none():
                raise ValueError('El área no está activa.')
            if not c.execute(text("SELECT g.id_grupo FROM grupos_academicos g JOIN ciclos_preparacion c ON c.id_ciclo=g.id_ciclo WHERE g.id_grupo=:id AND g.estado='ACTIVO' AND c.estado='ACTIVO' FOR UPDATE"), {"id": grupo}).scalar_one_or_none():
                raise ValueError('El grupo o ciclo no está activo.')
            for tabla, columna, valor in (("estudiante_area_historial", "id_area", area), ("estudiante_grupo_historial", "id_grupo", grupo)):
                actual = c.execute(text(f"SELECT {columna} AS valor,fecha_inicio FROM {tabla} WHERE id_estudiante=:id AND fecha_fin IS NULL FOR UPDATE"), {"id": id}).mappings().first()
                if not AsignacionAcademica.requiere_cambio(actual, valor, fecha):
                    continue
                if actual:
                    c.execute(text(f"UPDATE {tabla} SET fecha_fin=:fecha WHERE id_estudiante=:id AND fecha_fin IS NULL"), {"fecha": fecha, "id": id})
                c.execute(text(f"INSERT INTO {tabla}(id_estudiante,{columna},fecha_inicio) VALUES (:id,:valor,:fecha)"), {"id": id, "valor": valor, "fecha": fecha})

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

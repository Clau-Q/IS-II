#!/usr/bin/python
# -*- coding: utf-8 -*-
from dominio.organizacion_academica.estudiante import Estudiante

class EstudianteAppService:
    def __init__(self, repositorio=None):
        self.repositorio = repositorio

    def registrar_estudiante(self, datos):
        self.repositorio.guardar(self.validar(datos))

    def validar(self, datos):
        return Estudiante.validar_datos(datos)

    def listar(self, busqueda=""):
        return self.repositorio.listar({"busqueda": busqueda.strip()})

    def actualizar(self, id, datos):
        return self.repositorio.actualizar(id, self.validar(datos))

    def cambiar_estado(self, id, estado):
        return self.repositorio.cambiar_estado(id, Estudiante.validar_estado(estado))

    def buscar_por_id(self, id):
        return self.repositorio.buscar_por_id(id)

    def cambiar_asignacion(self, id, grupo, area, fecha):
        fecha, area, grupo = Estudiante.validar_cambio(fecha, area, grupo)
        self.repositorio.cambiar_asignacion(id, grupo, area, fecha)

    def consultar_asignaciones(self, id):
        return self.repositorio.consultar_asignaciones(id)

    def vincular_cuenta(self, id, cuenta_id):
        return self.repositorio.vincular_cuenta(id, cuenta_id.strip())

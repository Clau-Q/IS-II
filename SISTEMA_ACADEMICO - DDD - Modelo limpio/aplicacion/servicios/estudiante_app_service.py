#!/usr/bin/python
# -*- coding: utf-8 -*-

class EstudianteAppService:
    def __init__(self, repositorio=None):
        self.repositorio = repositorio

    def registrar_estudiante(self, datos):
        self.repositorio.guardar(self.validar(datos))

    def validar(self, datos):
        valores = {campo: datos.get(campo, "").strip() for campo in ("codigo", "nombres", "apellidos", "dni", "email", "telefono")}
        if not all(valores[campo] for campo in ("codigo", "nombres", "apellidos")):
            raise ValueError("Código, nombres y apellidos son obligatorios.")
        for campo in ("dni", "email", "telefono"):
            valores[campo] = valores[campo] or None
        return valores

    def listar(self, busqueda=""):
        return self.repositorio.listar({"busqueda": busqueda.strip()})

    def actualizar(self, id, datos):
        return self.repositorio.actualizar(id, self.validar(datos))

    def cambiar_estado(self, id, estado):
        if estado not in ("ACTIVO", "INACTIVO"):
            raise ValueError("Estado no válido.")
        return self.repositorio.cambiar_estado(id, estado)

    def cambiar_asignacion(self, id, grupo, area, fecha):
        pass

    def vincular_cuenta(self, id, cuenta_id):
        return self.repositorio.vincular_cuenta(id, cuenta_id.strip())

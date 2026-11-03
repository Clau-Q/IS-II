#!/usr/bin/python
# -*- coding: utf-8 -*-

class Simulacro:
    def __init__(self):
        self.id = None
        self.ciclo_id = None
        self.nombre = None
        self.fecha_aplicacion = None
        self.estado = None
        self.examenes_por_area = None

    def registrar_examen(self, area_id, examen_id):
        pass

    def actualizar_datos(self, cambios):
        pass

    def desactivar(self, motivo):
        pass

    def confirmar(self):
        pass

#!/usr/bin/python
# -*- coding: utf-8 -*-

class Examen:
    def __init__(self):
        self.id = None
        self.simulacro_id = None
        self.area_id = None
        self.fecha_aplicacion = None
        self.puntaje_maximo = None
        self.estado = None
        self.conjunto_calificacion_activo_id_opcional = None

    def configurar_distribucion(self):
        pass

    def generar_cuadernillo_unico(self):
        pass

    def aprobar_estructura(self):
        pass

    def confirmar_conjunto(self, clave_id, politica_id, responsable_id):
        pass

    def validar_items_y_versiones(self):
        pass

    def validar_estructura_para_aprobar(self):
        pass

    def retirar(self, motivo, responsable_id):
        pass

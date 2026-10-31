#!/usr/bin/python
# -*- coding: utf-8 -*-

class Participacion:
    def __init__(self):
        self.id = None
        self.estudiante_id = None
        self.simulacro_id = None
        self.examen_id = None
        self.cartilla_vigente_id_opcional = None
        self.estado = None
        self.ultimo_calculo_id_opcional = None

    def recibir_cartilla(self, imagen, cuadernillo_id):
        pass

    def reemplazar_cartilla(self, imagen, cuadernillo_id, motivo):
        pass

    def registrar_lectura(self, cartilla_id):
        pass

    def confirmar_lectura(self, lectura_id):
        pass

    def invalidar_cartilla(self, cartilla_id, rectificacion_id):
        pass

    def validar_simulacro_del_examen(self, simulacro_examen_id):
        pass

#!/usr/bin/python
# -*- coding: utf-8 -*-

class CalculoResultado:
    def __init__(self):
        self.id = None
        self.participacion_id = None
        self.cartilla_id = None
        self.lectura_id = None
        self.revision_clave_id = None
        self.revision_politica_id = None
        self.conjunto_id = None
        self.puntaje_total = None
        self.aciertos = None
        self.incorrectas = None
        self.blancos = None
        self.estado_revision = None
        self.calculado_por = None
        self.calculado_en = None
        self.revisado_por_opcional = None
        self.revisado_en_opcional = None

    def marcar_revisado(self):
        pass

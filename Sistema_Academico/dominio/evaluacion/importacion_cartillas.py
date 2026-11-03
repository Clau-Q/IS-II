#!/usr/bin/python
# -*- coding: utf-8 -*-

class ImportacionCartillas:
    def __init__(self):
        self.id = None
        self.examen_destino_id = None
        self.operacion_id = None
        self.responsable_id = None
        self.creada_en = None

    def agregar_entrada(self, fuente, pagina):
        pass

    def resolver_identificacion(self, entrada_id, estudiante_id, cuadernillo_id):
        pass

    def reintentar_entrada(self, entrada_id, operacion_id):
        pass

    def descartar_entrada(self, entrada_id, motivo, responsable_id):
        pass

    def aportar_reemplazo_legible(self, entrada_id, archivo):
        pass

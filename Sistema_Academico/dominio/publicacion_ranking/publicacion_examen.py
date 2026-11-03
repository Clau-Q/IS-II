#!/usr/bin/python
# -*- coding: utf-8 -*-

class PublicacionExamen:
    def __init__(self):
        self.id = None
        self.examen_id = None
        self.simulacro_id = None
        self.area_id = None
        self.ciclo_id = None
        self.fecha_aplicacion = None
        self.puntaje_maximo = None
        self.rectificacion_id_opcional = None
        self.publicada_en = None
        self.responsable_id = None
        self.motivo = None
        self.version_publicacion = None

    def actualizar_resultados_vigentes(self, resultados, publicada_en, motivo):
        pass

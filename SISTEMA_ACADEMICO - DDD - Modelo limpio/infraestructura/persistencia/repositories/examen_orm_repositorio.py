#!/usr/bin/python
# -*- coding: utf-8 -*-

from dominio.diseno_evaluaciones.i_examen_repositorio import IExamenRepositorio


class ExamenORMRepositorio(IExamenRepositorio):

    def guardar(self, examen):
        pass

    def buscar_por_id(self, id):
        pass

    def listar(self, filtros):
        pass

    def buscar_por_simulacro_y_area(self, simulacro_id, area_id):
        pass

    def __init__(self, session):
        self.session = session

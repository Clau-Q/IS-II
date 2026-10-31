#!/usr/bin/python
# -*- coding: utf-8 -*-

from dominio.evaluacion.i_participacion_repositorio import IParticipacionRepositorio


class ParticipacionORMRepositorio(IParticipacionRepositorio):

    def guardar(self, participacion):
        pass

    def buscar_por_id(self, id):
        pass

    def listar(self, filtros):
        pass

    def guardar_con_unicidad(self, participacion):
        pass

    def buscar_por_estudiante_y_simulacro(self, estudiante_id, simulacro_id):
        pass

    def __init__(self, session):
        self.session = session

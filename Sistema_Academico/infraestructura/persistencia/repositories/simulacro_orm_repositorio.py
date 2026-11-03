#!/usr/bin/python
# -*- coding: utf-8 -*-

from dominio.diseno_evaluaciones.i_simulacro_repositorio import ISimulacroRepositorio


class SimulacroORMRepositorio(ISimulacroRepositorio):

    def guardar(self, simulacro):
        pass

    def buscar_por_id(self, id):
        pass

    def listar(self, filtros):
        pass

    def __init__(self, session):
        self.session = session

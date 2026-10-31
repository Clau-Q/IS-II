#!/usr/bin/python
# -*- coding: utf-8 -*-

from dominio.evaluacion.i_calculo_repositorio import ICalculoRepositorio


class CalculoResultadoORMRepositorio(ICalculoRepositorio):

    def guardar(self, calculo_resultado):
        pass

    def buscar_por_id(self, id):
        pass

    def listar(self, filtros):
        pass

    def registrar_nueva_version(self, calculo_resultado):
        pass

    def __init__(self, session):
        self.session = session

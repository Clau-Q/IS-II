#!/usr/bin/python
# -*- coding: utf-8 -*-

from dominio.banco_preguntas.i_pregunta_repositorio import IPreguntaRepositorio


class PreguntaORMRepositorio(IPreguntaRepositorio):

    def guardar(self, pregunta):
        pass

    def buscar_por_id(self, id):
        pass

    def listar(self, filtros):
        pass

    def __init__(self, session):
        self.session = session

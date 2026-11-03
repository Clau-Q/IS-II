#!/usr/bin/python
# -*- coding: utf-8 -*-

from dominio.organizacion_academica.i_eje_tematico_repositorio import IEjeTematicoRepositorio


class EjeTematicoORMRepositorio(IEjeTematicoRepositorio):

    def guardar(self, eje_tematico):
        pass

    def buscar_por_id(self, id):
        pass

    def listar(self, filtros):
        pass

    def __init__(self, session):
        self.session = session

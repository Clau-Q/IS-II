#!/usr/bin/python
# -*- coding: utf-8 -*-

from dominio.organizacion_academica.i_ciclo_repositorio import ICicloRepositorio


class CicloORMRepositorio(ICicloRepositorio):

    def guardar(self, ciclo):
        pass

    def buscar_por_id(self, id):
        pass

    def listar(self, filtros):
        pass

    def __init__(self, session):
        self.session = session

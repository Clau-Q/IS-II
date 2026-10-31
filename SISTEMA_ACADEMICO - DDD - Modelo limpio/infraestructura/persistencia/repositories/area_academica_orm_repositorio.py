#!/usr/bin/python
# -*- coding: utf-8 -*-

from dominio.organizacion_academica.i_area_academica_repositorio import IAreaAcademicaRepositorio


class AreaAcademicaORMRepositorio(IAreaAcademicaRepositorio):

    def guardar(self, area_academica):
        pass

    def buscar_por_id(self, id):
        pass

    def listar(self, filtros):
        pass

    def __init__(self, session):
        self.session = session

#!/usr/bin/python
# -*- coding: utf-8 -*-

from dominio.organizacion_academica.i_docente_repositorio import IDocenteRepositorio


class DocenteORMRepositorio(IDocenteRepositorio):

    def guardar(self, docente):
        pass

    def buscar_por_id(self, id):
        pass

    def listar(self, filtros):
        pass

    def __init__(self, session):
        self.session = session

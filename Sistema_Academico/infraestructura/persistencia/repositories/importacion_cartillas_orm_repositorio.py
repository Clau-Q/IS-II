#!/usr/bin/python
# -*- coding: utf-8 -*-

from dominio.evaluacion.i_importacion_cartillas_repositorio import IImportacionCartillasRepositorio


class ImportacionCartillasORMRepositorio(IImportacionCartillasRepositorio):

    def guardar(self, importacion_cartillas):
        pass

    def buscar_por_id(self, id):
        pass

    def listar(self, filtros):
        pass

    def registrar_nueva_version(self, importacion_cartillas):
        pass

    def __init__(self, session):
        self.session = session

#!/usr/bin/python
# -*- coding: utf-8 -*-

from dominio.publicacion_ranking.i_publicacion_repositorio import IPublicacionRepositorio


class PublicacionExamenORMRepositorio(IPublicacionRepositorio):

    def guardar(self, publicacion_examen):
        pass

    def buscar_por_id(self, id):
        pass

    def listar(self, filtros):
        pass

    def obtener_vigente(self, examen_id):
        pass

    def __init__(self, session):
        self.session = session

    def guardar_vigente(self, publicacion):
        pass

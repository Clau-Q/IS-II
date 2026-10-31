#!/usr/bin/python
# -*- coding: utf-8 -*-

from aplicacion.puertos.i_lector_cartillas import ILectorCartillas


class LectorBurbujasOpenCV(ILectorCartillas):
    def __init__(self):
        self.version_algoritmo = None
        self.umbral_revision = None
        self.requiere_plantilla = None

    def leer(self, imagen_ref, plantilla_ref):
        pass

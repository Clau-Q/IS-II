#!/usr/bin/python
# -*- coding: utf-8 -*-

from aplicacion.puertos.i_unidad_trabajo import IUnidadTrabajo


class UnidadTrabajoSQLAlchemy(IUnidadTrabajo):
    def __init__(self):
        self.session = None

    def iniciar(self):
        pass

    def confirmar(self):
        pass

    def revertir(self):
        pass

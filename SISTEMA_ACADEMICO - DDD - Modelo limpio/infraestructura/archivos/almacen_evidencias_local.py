#!/usr/bin/python
# -*- coding: utf-8 -*-

from aplicacion.puertos.i_almacen_evidencias import IAlmacenEvidencias


class AlmacenEvidenciasLocal(IAlmacenEvidencias):
    def __init__(self):
        self.directorio_privado = None
        self.max_bytes = None

    def guardar(self, archivo, operacion_id):
        pass

    def abrir(self, referencia):
        pass

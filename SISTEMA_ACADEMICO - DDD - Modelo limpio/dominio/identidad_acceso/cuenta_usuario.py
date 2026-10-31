#!/usr/bin/python
# -*- coding: utf-8 -*-

class CuentaUsuario:
    def __init__(self):
        self.id = None
        self.nombre_usuario = None
        self.password_hash = None
        self.roles = None
        self.activa = None

    def asignar_roles(self, roles):
        pass

    def desactivar(self):
        pass

    def activar(self):
        pass

    def cambiar_credencial(self, nuevo_hash):
        pass

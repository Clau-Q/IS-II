#!/usr/bin/python
# -*- coding: utf-8 -*-

class CuentaUsuarioAppService:
    def __init__(self, repositorio=None, protector=None):
        self.repositorio = repositorio
        self.protector = protector

    def registrar_cuenta(self, datos):
        pass

    def asignar_roles(self, cuenta_id, roles):
        pass

    def iniciar_sesion(self, usuario, credencial):
        cuenta = self.repositorio.buscar_por_nombre(usuario.strip())
        if not cuenta or not cuenta["activa"] or not self.protector.verificar(cuenta["password_hash"], credencial):
            return None
        return cuenta

    def recuperar_acceso(self, solicitud):
        pass

    def registrar_con_clave(self, datos, contrasena):
        pass

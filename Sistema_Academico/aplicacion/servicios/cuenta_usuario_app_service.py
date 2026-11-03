#!/usr/bin/python
# -*- coding: utf-8 -*-

class CuentaUsuarioAppService:
    def __init__(self, repositorio=None, protector=None):
        self.repositorio = repositorio
        self.protector = protector

    def registrar_cuenta(self, datos):
        raise NotImplementedError('El registro de cuentas se realiza mediante GestionUsuariosAppService.')

    def asignar_roles(self, cuenta_id, roles):
        raise NotImplementedError('La modificación de roles existentes aún no está implementada.')

    def iniciar_sesion(self, usuario, credencial):
        cuenta = self.repositorio.buscar_por_nombre(usuario.strip())
        if not cuenta or not cuenta["activa"] or not self.protector.verificar(cuenta["password_hash"], credencial):
            return None
        return cuenta

    def consultar_cuenta_activa(self, usuario):
        cuenta = self.repositorio.buscar_por_nombre(usuario)
        return cuenta if cuenta and cuenta['activa'] else None

    def recuperar_acceso(self, solicitud):
        raise NotImplementedError('La recuperación de acceso está pendiente de definir.')

    def registrar_con_clave(self, datos, contrasena):
        raise NotImplementedError('El registro de cuentas se realiza mediante GestionUsuariosAppService.')

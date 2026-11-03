#!/usr/bin/python
# -*- coding: utf-8 -*-

class Autorizacion:
    @staticmethod
    def puede_acceder(roles, requerido):
        return requerido in roles or (requerido == 'COORDINADOR' and 'DIRECTOR' in roles)

    @staticmethod
    def validar_roles(roles, director):
        if not roles or any(r not in ('ESTUDIANTE', 'DOCENTE', 'COORDINADOR', 'DIRECTOR') for r in roles) or len(set(roles)) != len(roles):
            raise ValueError('Roles no válidos.')
        if 'ESTUDIANTE' in roles and len(roles) != 1:
            raise ValueError('El rol estudiante no se puede combinar con otros roles.')
        if 'DIRECTOR' in roles and not director:
            raise PermissionError('Solo un director puede asignar el rol director.')

    @staticmethod
    def validar_modificacion_cuenta(es_director, actor_director):
        if es_director and not actor_director:
            raise PermissionError('Solo un director puede modificar cuentas de director.')

    def __init__(self):
        pass

    def verificar_permiso(self, cuenta, operacion):
        pass

    def verificar_acceso_a_resultado(self, cuenta, estudiante_id):
        pass

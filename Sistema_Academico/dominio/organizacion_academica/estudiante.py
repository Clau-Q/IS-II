#!/usr/bin/python
# -*- coding: utf-8 -*-

class Estudiante:
    @staticmethod
    def validar_datos(datos):
        valores = {campo: str(datos.get(campo) or '').strip() for campo in ('codigo', 'nombres', 'apellidos', 'dni', 'email', 'telefono')}
        if not all(valores[campo] for campo in ('codigo', 'nombres', 'apellidos')):
            raise ValueError('Código, nombres y apellidos son obligatorios.')
        for campo in ('dni', 'email', 'telefono'):
            valores[campo] = valores[campo] or None
        return valores

    @staticmethod
    def validar_estado(estado):
        if estado not in ('ACTIVO', 'INACTIVO'):
            raise ValueError('Estado no válido.')
        return estado

    @staticmethod
    def validar_cambio(fecha, area_id, grupo_id):
        from datetime import date
        try:
            fecha_valida = date.fromisoformat(fecha)
            area_id, grupo_id = int(area_id), int(grupo_id)
        except (TypeError, ValueError):
            raise ValueError('Selecciona una fecha, un área y un grupo válidos.') from None
        if area_id <= 0 or grupo_id <= 0:
            raise ValueError('Selecciona un área y un grupo válidos.')
        if fecha_valida > date.today():
            raise ValueError('La fecha del cambio no puede ser futura.')
        return fecha_valida, area_id, grupo_id

    def __init__(self):
        self.id = None
        self.codigo = None
        self.nombres = None
        self.cuenta_id_opcional = None
        self.activo = None

    def cambiar_asignacion(self, grupo_id, area_id, fecha):
        pass

    def vincular_cuenta(self, cuenta_id):
        pass

    def desactivar(self):
        pass

    def activar(self):
        pass

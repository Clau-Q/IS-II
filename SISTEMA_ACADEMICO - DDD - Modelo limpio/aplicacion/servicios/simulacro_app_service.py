#!/usr/bin/python
# -*- coding: utf-8 -*-

class SimulacroAppService:
    def __init__(self, repositorio):
        self.repositorio = repositorio

    def crear_simulacro(self, datos, usuario_id):
        from datetime import date
        nombre = datos.get('nombre', '').strip()
        if not nombre or len(nombre) > 150:
            raise ValueError('Ingresa un nombre de hasta 150 caracteres.')
        try:
            fecha = date.fromisoformat(datos.get('fecha', ''))
            ciclo = int(datos.get('ciclo', ''))
        except ValueError:
            raise ValueError('Selecciona un ciclo y una fecha válidos.') from None
        areas = self._validar_areas(datos.get('areas', []))
        if ciclo <= 0:
            raise ValueError('Selecciona un ciclo válido.')
        self.repositorio.crear_simulacro({'nombre': nombre, 'fecha': fecha, 'ciclo': ciclo, 'areas': areas}, usuario_id)

    @staticmethod
    def _validar_areas(valores):
        try:
            areas = [int(valor) for valor in valores]
        except (TypeError, ValueError):
            raise ValueError('Selecciona áreas válidas.') from None
        if not areas or any(area <= 0 for area in areas) or len(set(areas)) != len(areas):
            raise ValueError('Selecciona una o más áreas diferentes.')
        return areas

    def agregar_areas(self, simulacro, valores, usuario_id):
        try:
            simulacro = int(simulacro)
        except (TypeError, ValueError):
            raise ValueError('Selecciona un examen válido.') from None
        if simulacro <= 0:
            raise ValueError('Selecciona un examen válido.')
        self.repositorio.agregar_areas(simulacro, self._validar_areas(valores), usuario_id)

    def listar(self):
        return self.repositorio.simulacros()

    def contexto_examen(self, examen):
        return self.repositorio.contexto_examen(examen)

    def abrir_aplicacion(self, simulacro, examen=0):
        return self.repositorio.abrir_aplicacion(simulacro, examen)

    def resumen_examen(self, examen):
        return self.repositorio.resumen_examen(examen)

    def habilitar_preguntas(self, examen, accion):
        try:
            examen = int(examen)
        except (TypeError, ValueError):
            raise ValueError('Selecciona un examen válido.') from None
        if examen <= 0 or accion not in ('habilitar', 'cerrar'):
            raise ValueError('Acción no válida.')
        self.repositorio.habilitar_preguntas(examen, accion == 'habilitar')

    def crear_examen(self, datos, usuario_id):
        from datetime import date
        nombre = datos.get('nombre', '').strip()
        if not nombre or len(nombre) > 150:
            raise ValueError('Ingresa un nombre de hasta 150 caracteres.')
        try:
            fecha = date.fromisoformat(datos.get('fecha', ''))
            simulacro = int(datos.get('simulacro', ''))
            area = int(datos.get('area', ''))
        except ValueError:
            raise ValueError('Selecciona simulacro, área y fecha válidos.') from None
        self.repositorio.crear_examen({'nombre': nombre, 'fecha': fecha, 'simulacro': simulacro, 'area': area}, usuario_id)

    def confirmar_simulacro(self, simulacro_id):
        pass

    def desactivar_simulacro(self, id, motivo):
        pass

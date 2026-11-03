#!/usr/bin/python
# -*- coding: utf-8 -*-

from dominio.banco_preguntas.pregunta import Pregunta


class PreguntaAppService:
    def __init__(self, repositorio):
        self.repositorio = repositorio

    def crear_pregunta(self, datos):
        pass

    def editar_version(self, pregunta_id, datos):
        pass

    def enviar_revision(self, pregunta_id):
        pass

    def revisar_pregunta(self, pregunta_id, version_vista_id, accion, observacion, usuario_id):
        aprobar, observacion = Pregunta.validar_revision(accion, observacion)
        self.repositorio.revisar(pregunta_id, version_vista_id, aprobar, observacion, usuario_id)

    def consultar_banco(self, filtros):
        estado = filtros.get('estado', '')
        if estado not in ('', 'BORRADOR', 'REVISION', 'APROBADA', 'INACTIVA'):
            raise ValueError('Estado no válido.')
        try:
            materia = int(filtros.get('materia') or 0)
            area = int(filtros.get('area') or 0)
            eje = int(filtros.get('eje') or 0)
            examen = int(filtros.get('examen') or 0)
        except ValueError:
            raise ValueError('Filtros no válidos.') from None
        return self.repositorio.preguntas(estado, materia, area, eje, examen)

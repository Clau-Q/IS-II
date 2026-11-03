#!/usr/bin/python
# -*- coding: utf-8 -*-

class Pregunta:
    @staticmethod
    def validar_revision(accion, observacion):
        if accion not in ('aprobar', 'devolver'):
            raise ValueError('Acción de revisión no válida.')
        observacion = (observacion or '').strip()
        if accion == 'devolver' and not observacion:
            raise ValueError('Indica una observación para devolver la pregunta.')
        return accion == 'aprobar', observacion
    def __init__(self):
        self.id = None
        self.autor_id = None
        self.materia_id = None
        self.area_ids = None
        self.estado = None
        self.version_activa_id = None

    def enviar_a_revision(self):
        pass

    def aprobar_inicialmente(self, coordinador_id, version_vista_id):
        pass

    def devolver_a_borrador(self, motivo, version_vista_id):
        pass

    def editar_creando_version(self, contenido, responsable_id):
        pass

    def desactivar(self):
        pass

    def es_elegible_para_area(self, area_id):
        pass

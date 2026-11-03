#!/usr/bin/python
# -*- coding: utf-8 -*-
from aplicacion.puertos.i_panel_pendientes import IPanelPendientes

class PanelPendientesAppService:
    def __init__(self, repositorio: IPanelPendientes):
        self.repositorio = repositorio

    def consultar_pendientes(self, examen_id=None):
        return self.repositorio.consultar()

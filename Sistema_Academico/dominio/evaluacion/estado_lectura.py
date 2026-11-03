#!/usr/bin/python
# -*- coding: utf-8 -*-

from enum import Enum

class EstadoLectura(Enum):
    PENDIENTE_REVISION = 1
    CONFIRMADA = 2
    ESPERA_REEMPLAZO_LEGIBLE = 3
    OBSOLETA = 4

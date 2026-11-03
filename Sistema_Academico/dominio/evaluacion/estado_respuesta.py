#!/usr/bin/python
# -*- coding: utf-8 -*-

from enum import Enum

class EstadoRespuesta(Enum):
    PENDIENTE_REVISION = 1
    UNICA_CONFIRMADA = 2
    BLANCO_CONFIRMADO = 3
    MULTIPLE_CONFIRMADA = 4

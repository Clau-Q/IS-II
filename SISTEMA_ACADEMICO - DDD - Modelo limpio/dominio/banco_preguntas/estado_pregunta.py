#!/usr/bin/python
# -*- coding: utf-8 -*-

from enum import Enum

class EstadoPregunta(Enum):
    BORRADOR = 1
    EN_REVISION = 2
    APROBADA = 3
    INACTIVA = 4

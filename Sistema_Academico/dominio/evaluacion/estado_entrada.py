#!/usr/bin/python
# -*- coding: utf-8 -*-

from enum import Enum

class EstadoEntrada(Enum):
    PENDIENTE_IDENTIFICACION = 1
    ERROR_ARCHIVO = 2
    LISTA_PARA_REGISTRAR = 3
    REGISTRADA = 4
    ESPERA_REEMPLAZO_LEGIBLE = 5
    SUSTITUIDA = 6
    DESCARTADA_JUSTIFICADA = 7

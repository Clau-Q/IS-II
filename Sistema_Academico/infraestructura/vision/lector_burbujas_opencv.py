#!/usr/bin/python
# -*- coding: utf-8 -*-

from aplicacion.puertos.i_lector_cartillas import ILectorCartillas
from pathlib import Path
from tempfile import TemporaryDirectory
from shutil import copy2


class LectorBurbujasOpenCV(ILectorCartillas):
    def __init__(self):
        self.version_algoritmo = 'ADDISON OMR 0.5.4-experimental'
        self.umbral_revision = None  # La confianza del lector es cualitativa, no porcentual.
        self.requiere_plantilla = True

    def leer(self, imagen_ref, plantilla_ref):
        from infraestructura.vision.addison_omr import procesar

        imagen = Path(imagen_ref).resolve(strict=True)
        plantilla = Path(plantilla_ref).resolve(strict=True) if plantilla_ref else Path(__file__).parent / 'addison_omr'
        if not imagen.is_file() or not plantilla.is_dir():
            raise ValueError('La imagen o la carpeta de plantilla no son válidas.')

        # El motor escribe imágenes intermedias en su carpeta de trabajo.
        # Cada lectura recibe una copia aislada para evitar colisiones entre cargas.
        with TemporaryDirectory(prefix='addison_omr_') as temporal:
            trabajo = Path(temporal)
            for nombre in ('02_2_mapa_coordenadas_burbujas.json', '02_3_plantilla_maestra_sin_marcas.png'):
                origen = plantilla / nombre
                if not origen.is_file():
                    raise FileNotFoundError(f'Falta el recurso de plantilla: {nombre}')
                copy2(origen, trabajo / nombre)
            resultado = procesar(imagen, trabajo, salida=trabajo / 'lectura', alineacion=True, alineacion_local=True)
            if resultado.get('exito') is False:
                return {'exito': False, 'version_lector': self.version_algoritmo, 'error': resultado.get('error', 'Lectura rechazada'), 'detalle': resultado}
            return {
                'exito': True,
                'version_lector': self.version_algoritmo,
                'dni': resultado.get('dni'),
                'controles': resultado.get('controles', {}),
                'respuestas': resultado.get('respuestas', []),
                'resumen': resultado.get('resumen', {}),
                'detalle': resultado,
            }

#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from uuid import uuid4
from aplicacion.puertos.i_cargas_omr import ICargasOMR
from aplicacion.puertos.i_preparador_cartillas import IPreparadorCartillas
from aplicacion.puertos.i_lector_cartillas import ILectorCartillas
from dominio.evaluacion.identificacion_cartilla import identificar_cartilla


logger = logging.getLogger(__name__)


class ImportacionCartillasAppService:
    def __init__(self, repositorio: ICargasOMR, preparador: IPreparadorCartillas, lector: ILectorCartillas):
        self.repositorio = repositorio
        self.preparador = preparador
        self.lector = lector

    def examenes(self):
        return self.repositorio.examenes()

    def listar(self, examen_id, pagina=1, estado=''):
        if estado not in ('', 'PENDIENTE', 'REVISAR', 'ERROR', 'DESCARTADA', 'REGISTRADA'):
            raise ValueError('Estado de carga no válido.')
        return self.repositorio.listar(examen_id, pagina, estado)

    def resumen(self, examen_id):
        return self.repositorio.resumen(examen_id)

    def opciones_identificacion(self, examen_id):
        return self.repositorio.opciones_identificacion(examen_id)

    def identificar_para_vista(self, entrada, estudiantes, versiones, area):
        import json
        lectura = entrada.get('lectura_json')
        if isinstance(lectura, str):
            lectura = json.loads(lectura)
        identificacion = identificar_cartilla(lectura, estudiantes, versiones, area)
        # Una identificación ya guardada se conserva; no se reasigna desde una vista.
        if entrada.get('estudiante_id'):
            identificacion['estudiante'] = next((e for e in estudiantes if e['id_estudiante'] == entrada['estudiante_id']), None)
        if entrada.get('version_id'):
            identificacion['version'] = next((v for v in versiones if v['id_version'] == entrada['version_id']), None)
        return identificacion

    def importar_lote(self, examen_id, archivos, usuario_id):
        if not archivos:
            raise ValueError('Selecciona al menos un archivo.')
        if len(archivos) > 20:
            raise ValueError('Selecciona como máximo 20 archivos por carga.')
        creadas = 0
        for nombre, contenido in archivos:
            operacion = str(uuid4())
            if not contenido or len(contenido) > self.preparador.MAX_BYTES:
                raise ValueError('Cada archivo debe contener datos y tener un máximo de 20 MB.')
            original, _ = self.preparador.guardar_pagina(contenido)
            try:
                paginas = self.preparador.paginas(nombre, contenido)
                for pagina, imagen in paginas:
                    ruta, huella = self.preparador.guardar_pagina(imagen)
                    datos = {'examen': examen_id, 'usuario': usuario_id, 'operacion': operacion, 'nombre': nombre[:255], 'pagina': pagina, 'huella': huella, 'ruta': str(ruta), 'original': str(original)}
                    try:
                        entrada_id = self.repositorio.crear(datos)
                    except Exception:
                        self.preparador.descartar_archivo_temporal(ruta)
                        raise
                    if entrada_id is None:
                        self.preparador.descartar_archivo_temporal(ruta)
                        continue
                    creadas += 1
                    self._procesar(entrada_id, ruta)
            except ValueError as error:
                ruta, huella = self.preparador.guardar_pagina(contenido)
                datos = {'examen': examen_id, 'usuario': usuario_id, 'operacion': operacion, 'nombre': nombre[:255], 'pagina': 0, 'huella': huella, 'ruta': str(ruta), 'original': str(original)}
                entrada_id = self.repositorio.crear(datos)
                if entrada_id:
                    creadas += 1
                    self.repositorio.actualizar_lectura(entrada_id, 'ERROR', error=str(error))
                else:
                    self.preparador.descartar_archivo_temporal(ruta)
        return creadas

    def _procesar(self, entrada_id, ruta):
        try:
            lectura = self.lector.leer(ruta, None)
            if not lectura['exito']:
                self.repositorio.actualizar_lectura(entrada_id, 'ERROR', lectura, lectura.get('error'))
            else:
                # La identificación se deriva de la lectura al presentar o registrar la entrada.
                self.repositorio.actualizar_lectura(entrada_id, 'REVISAR', lectura)
        except Exception:
            logger.exception('Error procesando la entrada %s', entrada_id)
            self.repositorio.actualizar_lectura(entrada_id, 'ERROR', error='No fue posible leer la imagen; revisa el archivo y los registros del servidor.')

    def resolver_identificacion(self, entrada_id, estudiante_id, version_id):
        try:
            estudiante_id = int(estudiante_id)
            version_id = int(version_id)
        except (TypeError, ValueError):
            raise ValueError('Selecciona un estudiante y una versión válidos.') from None
        if estudiante_id <= 0 or version_id <= 0:
            raise ValueError('Selecciona un estudiante y una versión válidos.')
        self.repositorio.resolver_identificacion(entrada_id, estudiante_id, version_id)

    def registrar_cartilla(self, entrada_id, usuario_id, motivo):
        return self.repositorio.registrar_cartilla(entrada_id, usuario_id, (motivo or '').strip())

    def descartar_entrada(self, entrada_id, motivo):
        motivo = (motivo or '').strip()
        if not motivo:
            raise ValueError('Indica el motivo del descarte.')
        if not self.repositorio.descartar(entrada_id, motivo):
            raise ValueError('La entrada no existe o ya fue descartada.')

    def obtener(self, entrada_id):
        return self.repositorio.obtener(entrada_id)

    def historial(self, entrada_id):
        return self.repositorio.historial(entrada_id)

    def archivo_anterior(self, entrada_id, historial_id):
        return self.repositorio.archivo_anterior(entrada_id, historial_id)

    def reintentar_lectura(self, entrada_id, usuario, motivo):
        motivo = (motivo or '').strip()
        if not motivo:
            raise ValueError('Indica por qué reintentas la lectura.')
        ruta = self.repositorio.preparar_reintento(entrada_id, usuario, motivo)
        self._procesar(entrada_id, ruta)

    def reemplazar_imagen(self, entrada_id, usuario, motivo, nombre, contenido):
        motivo = (motivo or '').strip()
        if not motivo:
            raise ValueError('Indica el motivo del reemplazo.')
        from pathlib import Path
        if Path(nombre).suffix.lower() not in ('.png', '.jpg', '.jpeg'):
            raise ValueError('Adjunta una imagen PNG o JPG de reemplazo.')
        paginas = list(self.preparador.paginas(nombre, contenido))
        ruta, huella = self.preparador.guardar_pagina(paginas[0][1])
        try:
            self.repositorio.preparar_reintento(entrada_id, usuario, motivo, {'ruta': str(ruta), 'huella': huella, 'nombre': Path(nombre).name[:255]})
        except Exception:
            self.preparador.descartar_archivo_temporal(ruta)
            raise
        self._procesar(entrada_id, ruta)

    def recibir_archivo(self, examen_id, archivo, operacion_id):
        pass

    def procesar_entrada(self, entrada_id, plantilla_ref):
        pass

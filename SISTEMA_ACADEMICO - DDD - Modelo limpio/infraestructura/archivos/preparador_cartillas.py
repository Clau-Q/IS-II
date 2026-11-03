"""Convierte documentos de entrada a imágenes independientes para el lector."""
from pathlib import Path
import hashlib
import uuid


class PreparadorCartillas:
    MAX_BYTES = 20 * 1024 * 1024
    MAX_PAGINAS = 100

    def __init__(self, directorio):
        self.directorio = Path(directorio).resolve()
        self.directorio.mkdir(parents=True, exist_ok=True)

    def paginas(self, nombre, contenido):
        if not contenido or len(contenido) > self.MAX_BYTES:
            raise ValueError('El archivo está vacío o supera 20 MB.')
        extension = Path(nombre).suffix.lower()
        if extension == '.pdf':
            import fitz
            try:
                documento = fitz.open(stream=contenido, filetype='pdf')
                with documento:
                    if documento.needs_pass or not documento.page_count or documento.page_count > self.MAX_PAGINAS:
                        raise ValueError('El PDF está vacío, requiere contraseña o supera 100 páginas.')
                    for numero, pagina in enumerate(documento, 1):
                        yield numero, pagina.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False).tobytes('png')
            except (RuntimeError, fitz.FileDataError) as error:
                raise ValueError('No se pudo abrir el PDF.') from error
        elif extension in ('.jpg', '.jpeg', '.png'):
            import cv2
            import numpy as np
            if cv2.imdecode(np.frombuffer(contenido, dtype=np.uint8), cv2.IMREAD_GRAYSCALE) is None:
                raise ValueError('La imagen no se pudo leer.')
            yield 1, contenido
        else:
            raise ValueError('Solo se admiten imágenes JPG, PNG o archivos PDF.')

    def guardar_pagina(self, contenido):
        huella = hashlib.sha256(contenido).hexdigest()
        ruta = self.directorio / (uuid.uuid4().hex + '.img')
        ruta.write_bytes(contenido)
        return ruta, huella

    def descartar_archivo_temporal(self, ruta):
        Path(ruta).unlink(missing_ok=True)

"""Normaliza imágenes para evitar conservar archivos no correspondientes."""
import uuid
from pathlib import Path
import cv2
import numpy as np


class ImagenesPreguntas:
    MAX_BYTES = 2 * 1024 * 1024

    def __init__(self, directorio):
        self.directorio = Path(directorio).resolve()
        self.directorio.mkdir(parents=True, exist_ok=True)

    def guardar(self, archivo):
        contenido = archivo.read(self.MAX_BYTES + 1)
        if not contenido or len(contenido) > self.MAX_BYTES:
            raise ValueError('Cada imagen debe contener datos y pesar como máximo 2 MB.')
        if Path(archivo.filename).suffix.lower() not in ('.jpg', '.jpeg', '.png'):
            raise ValueError('Solo se aceptan imágenes JPG o PNG.')
        imagen = cv2.imdecode(np.frombuffer(contenido, dtype=np.uint8), cv2.IMREAD_COLOR)
        if imagen is None or imagen.shape[0] * imagen.shape[1] > 16000000:
            raise ValueError('La imagen no es válida o supera las dimensiones permitidas.')
        exito, png = cv2.imencode('.png', imagen)
        if not exito:
            raise ValueError('No se pudo preparar la imagen.')
        ruta = self.directorio / (uuid.uuid4().hex + '.png')
        ruta.write_bytes(png.tobytes())
        return str(ruta), len(png) // 1024

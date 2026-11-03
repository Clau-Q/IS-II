"""Identificación de una cartilla a partir de marcas y coincidencias inequívocas."""
import re
import unicodedata


def _normalizar(valor):
    return ''.join(c for c in unicodedata.normalize('NFKD', str(valor)) if not unicodedata.combining(c)).casefold().strip()


def _control_valido(control):
    return (isinstance(control, dict) and control.get('estado') == 'VALIDA'
            and control.get('requiere_revision_manual') is not True
            and control.get('confianza') != 'baja' and bool(control.get('respuesta')))


def identificar_cartilla(lectura, estudiantes, versiones, area_actual):
    resultado = {'estudiante': None, 'version': None, 'area_detectada': None,
                 'area_coincide': False, 'bloqueo': None, 'completa': False}
    if not lectura or not lectura.get('exito'):
        return resultado
    resumen = lectura.get('resumen') or {}
    detalle = lectura.get('detalle') or {}
    dni = str(lectura.get('dni') or '').strip()
    columnas = lectura.get('detalle_dni') or detalle.get('detalle_dni') or []
    dni_valido = (bool(re.fullmatch(r'[0-9]{8}', dni)) and resumen.get('dni_completo') is True
                  and not resumen.get('dni_columnas_revision') and not resumen.get('dni_faltantes_o_invalidos'))
    if columnas:
        dni_valido = dni_valido and len(columnas) == 8 and all(_control_valido(c) for c in columnas)
    if dni_valido:
        coincidencias = [e for e in estudiantes if str(e.get('dni') or '').strip() == dni]
        if len(coincidencias) == 1:
            resultado['estudiante'] = coincidencias[0]

    controles = lectura.get('controles') or {}
    area = controles.get('area') or {}
    if _control_valido(area) and 'area' not in (resumen.get('controles_revision') or []):
        mapa = {'I': 'Ingenierías', 'B': 'Biomédicas', 'S': 'Sociales'}
        nombre = mapa.get(str(area['respuesta']).upper())
        if nombre:
            resultado['area_detectada'] = nombre
            resultado['area_coincide'] = _normalizar(nombre) == _normalizar(area_actual)
            if not resultado['area_coincide']:
                resultado['bloqueo'] = f'La cartilla indica {nombre}, pero la carga pertenece a {area_actual}. Cárgala en el área correspondiente o revisa la imagen.'

    tema = controles.get('tema') or {}
    if _control_valido(tema) and 'tema' not in (resumen.get('controles_revision') or []):
        codigo = str(tema['respuesta']).strip().upper()
        coincidencias = [v for v in versiones if str(v['codigo_version']).strip().upper() == codigo]
        if len(coincidencias) == 1:
            resultado['version'] = coincidencias[0]
        else:
            resultado['bloqueo'] = f'La cartilla indica la versión {codigo}, que no está activa en este examen. Revisa la imagen o la configuración.'
    elif len(versiones) == 1:
        resultado['version'] = versiones[0]

    resultado['completa'] = bool(resultado['estudiante'] and resultado['version']
                                 and resultado['area_coincide'] and not resultado['bloqueo'])
    return resultado

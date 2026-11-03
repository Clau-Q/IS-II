"""Reglas de integridad para el contenido que registra el docente."""


def validar_contenido(datos):
    enunciado = (datos.get('enunciado') or '').strip()
    respuesta = (datos.get('respuesta') or '').strip().upper()
    alternativas = {letra: (datos.get('alternativa_' + letra) or '').strip() for letra in 'ABCDE'}
    if not enunciado or len(enunciado) > 20000:
        raise ValueError('Escribe un enunciado de hasta 20 000 caracteres.')
    if any(len(valor) > 10000 for valor in alternativas.values()):
        raise ValueError('Cada alternativa admite hasta 10 000 caracteres.')
    if sum(bool(valor) for valor in alternativas.values()) < 2:
        raise ValueError('Registra al menos dos alternativas con texto.')
    if respuesta not in alternativas or not alternativas[respuesta]:
        raise ValueError('Selecciona como correcta una alternativa registrada.')
    return enunciado, respuesta, alternativas

"""Reglas compartidas para administrar la organización académica."""
from datetime import date


TIPOS = ('areas', 'ejes', 'materias', 'ciclos', 'grupos')


def identificador(valor, nombre):
    try:
        numero = int(valor)
    except (TypeError, ValueError):
        raise ValueError(f'Selecciona {nombre} válido.') from None
    if numero <= 0:
        raise ValueError(f'Selecciona {nombre} válido.')
    return numero


def validar_datos(tipo, datos):
    if tipo not in TIPOS:
        raise ValueError('Tipo de elemento no válido.')
    nombre = (datos.get('nombre') or '').strip()
    if not nombre or len(nombre) > 100:
        raise ValueError('El nombre es obligatorio y admite hasta 100 caracteres.')
    codigo = (datos.get('codigo') or '').strip()
    if tipo == 'areas' and (not codigo or len(codigo) > 50):
        raise ValueError('El código del área es obligatorio y admite hasta 50 caracteres.')
    valores = {'nombre': nombre, 'codigo': codigo}
    if tipo == 'materias':
        valores['id_eje'] = identificador(datos.get('id_eje'), 'un eje')
    if tipo == 'grupos':
        valores['id_ciclo'] = identificador(datos.get('id_ciclo'), 'un ciclo')
        for campo, maximo in (('horario', 100), ('aula', 50)):
            valor = (datos.get(campo) or '').strip()
            if len(valor) > maximo:
                raise ValueError(f'{campo.capitalize()} admite hasta {maximo} caracteres.')
            valores[campo] = valor or None
    if tipo == 'ciclos':
        try:
            inicio = date.fromisoformat(datos['fecha_inicio']) if datos.get('fecha_inicio') else None
            fin = date.fromisoformat(datos['fecha_fin']) if datos.get('fecha_fin') else None
        except ValueError:
            raise ValueError('Las fechas del ciclo no son válidas.') from None
        if inicio and fin and fin < inicio:
            raise ValueError('La fecha final no puede ser anterior a la inicial.')
        valores.update(fecha_inicio=inicio, fecha_fin=fin)
    return valores


def validar_estado(tipo, estado):
    if tipo not in TIPOS or estado not in ('ACTIVO', 'INACTIVO', 'FINALIZADO'):
        raise ValueError('Estado no válido.')
    if estado == 'FINALIZADO' and tipo != 'ciclos':
        raise ValueError('Solo se pueden finalizar ciclos.')
    return estado


def validar_transicion_estado(tipo, actual, nuevo):
    validar_estado(tipo, nuevo)
    if actual == 'FINALIZADO':
        raise ValueError('Un ciclo finalizado no puede reactivarse.')
    if actual not in ('ACTIVO', 'INACTIVO'):
        raise ValueError('Estado actual no válido.')

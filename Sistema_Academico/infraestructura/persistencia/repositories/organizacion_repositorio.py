"""Persistencia de catálogos académicos y asignaciones docentes."""
from sqlalchemy import text
from dominio.organizacion_academica.reglas_organizacion import validar_transicion_estado


class OrganizacionRepositorio:
    TABLAS = {
        'areas': ('areas', 'id_area', ('codigo', 'nombre')),
        'ejes': ('ejes_tematicos', 'id_eje', ('nombre',)),
        'materias': ('materias', 'id_materia', ('nombre', 'id_eje')),
        'ciclos': ('ciclos_preparacion', 'id_ciclo', ('nombre', 'fecha_inicio', 'fecha_fin')),
        'grupos': ('grupos_academicos', 'id_grupo', ('nombre', 'id_ciclo', 'horario', 'aula')),
    }

    def __init__(self, motor):
        self.motor = motor

    def listar(self):
        with self.motor.connect() as c:
            salida = {}
            for clave, (tabla, id_columna, columnas) in self.TABLAS.items():
                salida[clave] = c.execute(text(f"SELECT {id_columna} AS id, {','.join(columnas)}, estado FROM {tabla} ORDER BY nombre")).mappings().all()
            salida['docentes'] = c.execute(text("SELECT d.id_docente AS id, CONCAT(u.nombres,' ',u.apellidos) AS nombre FROM docentes d JOIN usuarios u ON u.id_usuario=d.id_usuario JOIN usuario_roles ur ON ur.id_usuario=u.id_usuario JOIN roles r ON r.id_rol=ur.id_rol AND r.nombre='DOCENTE' WHERE u.estado='ACTIVO' ORDER BY nombre")).mappings().all()
            salida['asignaciones'] = c.execute(text("""SELECT dm.id_docente,dm.id_materia,dm.estado,dm.fecha_asignacion,m.nombre materia,CONCAT(u.nombres,' ',u.apellidos) docente
                FROM docente_materias dm JOIN docentes d ON d.id_docente=dm.id_docente JOIN usuarios u ON u.id_usuario=d.id_usuario
                JOIN materias m ON m.id_materia=dm.id_materia ORDER BY docente,materia""")).mappings().all()
            return salida

    def _validar_padre(self, conexion, tipo, datos):
        if tipo == 'materias':
            padre = conexion.execute(text("SELECT id_eje FROM ejes_tematicos WHERE id_eje=:id AND estado='ACTIVO' FOR UPDATE"), {'id': datos['id_eje']}).scalar_one_or_none()
            if not padre:
                raise ValueError('El eje temático debe estar activo.')
        if tipo == 'grupos':
            padre = conexion.execute(text("SELECT id_ciclo FROM ciclos_preparacion WHERE id_ciclo=:id AND estado='ACTIVO' FOR UPDATE"), {'id': datos['id_ciclo']}).scalar_one_or_none()
            if not padre:
                raise ValueError('El ciclo debe estar activo.')

    def crear(self, tipo, datos):
        tabla, _, columnas = self.TABLAS[tipo]
        with self.motor.begin() as c:
            self._validar_padre(c, tipo, datos)
            c.execute(text(f"INSERT INTO {tabla} ({','.join(columnas)}) VALUES ({','.join(':'+n for n in columnas)})"), datos)

    def actualizar(self, tipo, id, datos):
        tabla, id_columna, columnas = self.TABLAS[tipo]
        with self.motor.begin() as c:
            actual = c.execute(text(f'SELECT * FROM {tabla} WHERE {id_columna}=:id FOR UPDATE'), {'id': id}).mappings().first()
            if not actual:
                raise ValueError('El elemento no existe.')
            if tipo == 'ciclos' and actual['estado'] == 'FINALIZADO':
                raise ValueError('No se modifica un ciclo finalizado.')
            for padre in ('id_eje', 'id_ciclo'):
                if padre in datos and datos[padre] != actual[padre]:
                    raise ValueError('La relación con el eje o ciclo se conserva para proteger el historial.')
            editables = [col for col in columnas if col not in ('id_eje', 'id_ciclo')]
            c.execute(text(f"UPDATE {tabla} SET {','.join(col+'=:'+col for col in editables)} WHERE {id_columna}=:id"), {**datos, 'id': id})

    def estado(self, tipo, id, estado):
        tabla, id_columna, _ = self.TABLAS[tipo]
        with self.motor.begin() as c:
            actual = c.execute(text(f'SELECT estado FROM {tabla} WHERE {id_columna}=:id FOR UPDATE'), {'id': id}).scalar_one_or_none()
            if actual is None:
                raise ValueError('El elemento no existe.')
            validar_transicion_estado(tipo, actual, estado)
            if tipo == 'materias' and estado == 'ACTIVO':
                activo = c.execute(text("SELECT COUNT(*) FROM materias m JOIN ejes_tematicos e ON e.id_eje=m.id_eje WHERE m.id_materia=:id AND e.estado='ACTIVO'"), {'id': id}).scalar_one()
                if not activo:
                    raise ValueError('Activa primero el eje de la materia.')
            if tipo == 'grupos' and estado == 'ACTIVO':
                activo = c.execute(text("SELECT COUNT(*) FROM grupos_academicos g JOIN ciclos_preparacion ci ON ci.id_ciclo=g.id_ciclo WHERE g.id_grupo=:id AND ci.estado='ACTIVO'"), {'id': id}).scalar_one()
                if not activo:
                    raise ValueError('El ciclo del grupo debe estar activo.')
            c.execute(text(f'UPDATE {tabla} SET estado=:estado WHERE {id_columna}=:id'), {'estado': estado, 'id': id})

    def asignar(self, docente, materia, activo):
        with self.motor.begin() as c:
            if not activo:
                actualizado = c.execute(text("UPDATE docente_materias SET estado='INACTIVO' WHERE id_docente=:docente AND id_materia=:materia AND estado='ACTIVO'"), {'docente': docente, 'materia': materia}).rowcount
                if not actualizado:
                    raise ValueError('La asignación no existe o ya está inactiva.')
                return
            docente_valido = c.execute(text("""SELECT d.id_docente FROM docentes d JOIN usuarios u ON u.id_usuario=d.id_usuario
                JOIN usuario_roles ur ON ur.id_usuario=u.id_usuario JOIN roles r ON r.id_rol=ur.id_rol AND r.nombre='DOCENTE'
                WHERE d.id_docente=:id AND u.estado='ACTIVO' FOR UPDATE"""), {'id': docente}).scalar_one_or_none()
            materia_valida = c.execute(text("SELECT m.id_materia FROM materias m JOIN ejes_tematicos e ON e.id_eje=m.id_eje WHERE m.id_materia=:id AND m.estado='ACTIVO' AND e.estado='ACTIVO' FOR UPDATE"), {'id': materia}).scalar_one_or_none()
            if not docente_valido or not materia_valida:
                raise ValueError('Selecciona un docente, una materia y un eje activos.')
            c.execute(text("INSERT INTO docente_materias(id_docente,id_materia,fecha_asignacion,estado) VALUES (:docente,:materia,CURRENT_DATE,'ACTIVO') ON DUPLICATE KEY UPDATE estado='ACTIVO'"), {'docente': docente, 'materia': materia})

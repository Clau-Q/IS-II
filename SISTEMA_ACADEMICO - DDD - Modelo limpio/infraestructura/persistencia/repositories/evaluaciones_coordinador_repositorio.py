from sqlalchemy import bindparam, text


class EvaluacionesCoordinadorRepositorio:
    def __init__(self, motor):
        self.motor = motor

    def contexto_examen(self, examen):
        with self.motor.connect() as c:
            fila = c.execute(text('''SELECT e.id_examen,e.id_simulacro,e.id_area,e.estado,e.admite_preguntas,
                a.nombre area,s.nombre nombre,s.fecha,cp.nombre ciclo,s.estado estado_aplicacion
                FROM examenes e JOIN simulacros s ON s.id_simulacro=e.id_simulacro
                JOIN areas a ON a.id_area=e.id_area JOIN ciclos_preparacion cp ON cp.id_ciclo=s.id_ciclo
                WHERE e.id_examen=:id'''), {'id': examen}).mappings().first()
            if not fila:
                return None
            areas = c.execute(text('''SELECT e.id_examen,a.nombre area FROM examenes e
                JOIN areas a ON a.id_area=e.id_area WHERE e.id_simulacro=:id ORDER BY a.nombre'''), {'id': fila['id_simulacro']}).mappings().all()
            return dict(fila, areas=areas)

    def abrir_aplicacion(self, simulacro, examen=0):
        with self.motor.connect() as c:
            ids = c.execute(text('SELECT id_examen FROM examenes WHERE id_simulacro=:id ORDER BY id_examen'), {'id': simulacro}).scalars().all()
        if not ids or (examen and examen not in ids):
            return None
        return self.contexto_examen(examen or ids[0])

    def resumen_examen(self, examen):
        with self.motor.connect() as c:
            resumen = dict(c.execute(text('''SELECT
                (SELECT COUNT(*) FROM preguntas p WHERE p.id_examen_destino=:id AND p.estado='REVISION') preguntas_revision,
                (SELECT COUNT(*) FROM versiones_examen WHERE id_examen=:id AND estado='ACTIVA') versiones,
                (SELECT COUNT(*) FROM cargas_omr WHERE examen_id=:id AND estado IN ('PENDIENTE','REVISAR','ERROR')) cargas_pendientes,
                (SELECT COUNT(*) FROM cartillas WHERE id_examen=:id AND vigente=1) cartillas,
                (SELECT COUNT(*) FROM cartillas WHERE id_examen=:id AND vigente=1 AND estado NOT IN ('VALIDADA','ANULADA')) cartillas_revision,
                (SELECT COUNT(*) FROM resultados_examen r JOIN cartillas ca ON ca.id_cartilla=r.id_cartilla
                    WHERE r.id_examen=:id AND r.vigente=1 AND ca.vigente=1) resultados,
                (SELECT COUNT(*) FROM resultados_examen r JOIN cartillas ca ON ca.id_cartilla=r.id_cartilla
                    WHERE r.id_examen=:id AND r.vigente=1 AND ca.vigente=1 AND r.estado='CALCULADO') calculos_revision,
                (SELECT COUNT(*) FROM resultados_examen r JOIN cartillas ca ON ca.id_cartilla=r.id_cartilla
                    WHERE r.id_examen=:id AND r.vigente=1 AND ca.vigente=1 AND r.estado='REVISADO') por_publicar,
                (SELECT COUNT(*) FROM publicaciones_examen WHERE id_examen=:id AND vigente=1) publicado
                '''), {'id': examen}).mappings().one())
            return resumen

    def simulacros(self):
        with self.motor.connect() as c:
            sims = c.execute(text("SELECT s.id_simulacro,s.nombre,s.fecha,s.estado,c.nombre AS ciclo FROM simulacros s JOIN ciclos_preparacion c ON c.id_ciclo=s.id_ciclo ORDER BY s.fecha DESC,s.id_simulacro DESC")).mappings().all()
            examenes = c.execute(text("SELECT e.id_examen,e.id_simulacro,e.nombre,e.estado,e.admite_preguntas,a.nombre AS area FROM examenes e JOIN areas a ON a.id_area=e.id_area ORDER BY e.nombre")).mappings().all()
            ciclos = c.execute(text("SELECT id_ciclo,nombre FROM ciclos_preparacion WHERE estado='ACTIVO' ORDER BY nombre")).mappings().all()
            areas = c.execute(text("SELECT id_area,nombre FROM areas WHERE estado='ACTIVO' ORDER BY nombre")).mappings().all()
            return sims, examenes, ciclos, areas

    def crear_simulacro(self, datos, usuario_id):
        with self.motor.begin() as c:
            if not c.execute(text("SELECT id_ciclo FROM ciclos_preparacion WHERE id_ciclo=:id AND estado='ACTIVO' FOR UPDATE"), {'id': datos['ciclo']}).scalar_one_or_none():
                raise ValueError('El ciclo seleccionado no está activo.')
            self._validar_areas(c, datos['areas'])
            simulacro = c.execute(text("INSERT INTO simulacros(id_ciclo,nombre,fecha,creado_por) VALUES (:ciclo,:nombre,:fecha,:usuario)"), {**datos, 'usuario': usuario_id}).lastrowid
            self._insertar_areas(c, simulacro, datos['nombre'], datos['fecha'], datos['areas'], usuario_id)

    @staticmethod
    def _validar_areas(c, areas):
        consulta = text("SELECT id_area FROM areas WHERE id_area IN :ids AND estado='ACTIVO' FOR UPDATE").bindparams(bindparam('ids', expanding=True))
        if set(c.execute(consulta, {'ids': areas}).scalars()) != set(areas):
            raise ValueError('Todas las áreas seleccionadas deben estar activas.')

    @staticmethod
    def _insertar_areas(c, simulacro, nombre, fecha, areas, usuario):
        for area in areas:
            c.execute(text("INSERT INTO examenes(id_simulacro,id_area,nombre,fecha_programada,creado_por) VALUES (:simulacro,:area,:nombre,:fecha,:usuario)"), {'simulacro': simulacro, 'area': area, 'nombre': nombre, 'fecha': fecha, 'usuario': usuario})

    def agregar_areas(self, simulacro, areas, usuario_id):
        with self.motor.begin() as c:
            evento = c.execute(text("SELECT nombre,fecha,estado FROM simulacros WHERE id_simulacro=:id FOR UPDATE"), {'id': simulacro}).mappings().first()
            if not evento or evento['estado'] != 'ABIERTO':
                raise ValueError('El examen no existe o está cerrado.')
            self._validar_areas(c, areas)
            existentes = set(c.execute(text('SELECT id_area FROM examenes WHERE id_simulacro=:id'), {'id': simulacro}).scalars())
            if existentes.intersection(areas):
                raise ValueError('Una de las áreas seleccionadas ya pertenece a este examen.')
            self._insertar_areas(c, simulacro, evento['nombre'], evento['fecha'], areas, usuario_id)

    def crear_examen(self, datos, usuario_id):
        with self.motor.begin() as c:
            if not c.execute(text("SELECT id_simulacro FROM simulacros WHERE id_simulacro=:id AND estado='ABIERTO' FOR UPDATE"), {'id': datos['simulacro']}).scalar_one_or_none():
                raise ValueError('El simulacro no está abierto.')
            if not c.execute(text("SELECT id_area FROM areas WHERE id_area=:id AND estado='ACTIVO' FOR UPDATE"), {'id': datos['area']}).scalar_one_or_none():
                raise ValueError('El área no está activa.')
            c.execute(text("INSERT INTO examenes(id_simulacro,id_area,nombre,fecha_programada,creado_por) VALUES (:simulacro,:area,:nombre,:fecha,:usuario)"), {**datos, 'usuario': usuario_id})

    def habilitar_preguntas(self, examen, habilitar):
        with self.motor.begin() as c:
            fila = c.execute(text("SELECT e.estado,s.estado simulacro FROM examenes e JOIN simulacros s ON s.id_simulacro=e.id_simulacro WHERE e.id_examen=:id FOR UPDATE"), {'id': examen}).mappings().first()
            if not fila:
                raise ValueError('El examen no existe.')
            if habilitar and (fila['estado'] not in ('BORRADOR', 'CONFIGURACION') or fila['simulacro'] != 'ABIERTO'):
                raise ValueError('Solo se puede habilitar un examen en configuración de un simulacro abierto.')
            c.execute(text('UPDATE examenes SET admite_preguntas=:habilitar WHERE id_examen=:id'), {'habilitar': habilitar, 'id': examen})

    def preguntas(self, estado, materia, area, eje, examen=0):
        with self.motor.connect() as c:
            filas = c.execute(text("""SELECT p.id_pregunta,p.estado,m.nombre AS materia,pv.id_version,pv.enunciado,pv.respuesta_correcta,CONCAT(u.nombres,' ',u.apellidos) AS autor
                FROM preguntas p JOIN materias m ON m.id_materia=p.id_materia
                JOIN pregunta_versiones pv ON pv.id_pregunta=p.id_pregunta AND pv.estado='ACTIVA'
                JOIN docentes d ON d.id_docente=p.id_autor_docente JOIN usuarios u ON u.id_usuario=d.id_usuario
                WHERE (:estado='' OR p.estado=:estado) AND (:materia=0 OR p.id_materia=:materia)
                AND (:eje=0 OR m.id_eje=:eje)
                AND (:area=0 OR EXISTS(SELECT 1 FROM pregunta_areas pa WHERE pa.id_pregunta=p.id_pregunta AND pa.id_area=:area))
                AND (:examen=0 OR p.id_examen_destino=:examen OR EXISTS (
                    SELECT 1 FROM examen_preguntas ep JOIN versiones_examen ve ON ve.id_version=ep.id_version_examen
                    JOIN pregunta_versiones vx ON vx.id_version=ep.id_version_pregunta
                    WHERE ve.id_examen=:examen AND vx.id_pregunta=p.id_pregunta))
                ORDER BY p.id_pregunta DESC LIMIT 200"""), {'estado': estado, 'materia': materia, 'area': area, 'eje': eje, 'examen': examen}).mappings().all()
            materias = c.execute(text("SELECT id_materia,nombre FROM materias ORDER BY nombre")).mappings().all()
            areas = c.execute(text("SELECT id_area,nombre FROM areas ORDER BY nombre")).mappings().all()
            ejes = c.execute(text("SELECT id_eje,nombre FROM ejes_tematicos ORDER BY nombre")).mappings().all()
            versiones = [fila['id_version'] for fila in filas]
            alternativas = {}
            if versiones:
                from sqlalchemy import bindparam
                consulta = text("SELECT id_version,letra,contenido FROM alternativas_pregunta WHERE id_version IN :versiones ORDER BY letra").bindparams(bindparam('versiones', expanding=True))
                for alternativa in c.execute(consulta, {'versiones': versiones}).mappings():
                    alternativas.setdefault(alternativa['id_version'], []).append(alternativa)
            imagenes = {}
            if versiones:
                consulta_imagenes = text("SELECT id_imagen,id_version,ubicacion,letra FROM pregunta_imagenes WHERE id_version IN :versiones ORDER BY orden,id_imagen").bindparams(bindparam('versiones', expanding=True))
                for imagen in c.execute(consulta_imagenes, {'versiones': versiones}).mappings():
                    imagenes.setdefault(imagen['id_version'], []).append(imagen)
            return [dict(fila, alternativas=alternativas.get(fila['id_version'], []), imagenes=imagenes.get(fila['id_version'], [])) for fila in filas], materias, areas, ejes

    def revisar(self, pregunta_id, version_id, aprobar, observacion, usuario_id):
        with self.motor.begin() as c:
            pregunta = c.execute(text("SELECT p.estado,pv.id_version,pv.sellada FROM preguntas p JOIN pregunta_versiones pv ON pv.id_pregunta=p.id_pregunta AND pv.estado='ACTIVA' WHERE p.id_pregunta=:id FOR UPDATE"), {'id': pregunta_id}).mappings().first()
            if not pregunta or pregunta['estado'] != 'REVISION' or pregunta['id_version'] != version_id:
                raise ValueError('La pregunta o su versión cambió; vuelve a consultar antes de revisarla.')
            if aprobar:
                c.execute(text("UPDATE preguntas SET estado='APROBADA', aprobado_por=:usuario WHERE id_pregunta=:id"), {'usuario': usuario_id, 'id': pregunta_id})
            else:
                c.execute(text("UPDATE preguntas SET estado='BORRADOR' WHERE id_pregunta=:id"), {'id': pregunta_id})
                c.execute(text("INSERT INTO revisiones_pregunta(id_version_pregunta,id_pregunta,id_usuario_revision,estado_anterior,estado_nuevo,observacion) VALUES (:version,:id,:usuario,'REVISION','BORRADOR',:observacion)"), {'version': version_id, 'id': pregunta_id, 'usuario': usuario_id, 'observacion': observacion})

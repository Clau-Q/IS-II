"""Almacenamiento transaccional de configuración y revisiones de clave."""
from sqlalchemy import bindparam, text
from dominio.diseno_evaluaciones.validador_examen import ValidadorExamen
from dominio.diseno_evaluaciones.examen import Examen


class DisenoExamenRepositorio:
    def __init__(self, motor):
        self.motor = motor

    def distribucion(self, examen):
        with self.motor.connect() as c:
            return c.execute(text('''SELECT m.nombre materia,et.nombre eje,d.cantidad_preguntas,
                d.puntaje_por_pregunta,d.puntaje_asignado FROM distribucion_examen d
                JOIN materias m ON m.id_materia=d.id_materia JOIN ejes_tematicos et ON et.id_eje=m.id_eje
                WHERE d.id_examen=:id ORDER BY d.orden,d.id_distribucion'''), {'id': examen}).mappings().all()

    def consultar(self, examen):
        with self.motor.connect() as c:
            examenes = c.execute(text('SELECT e.id_examen,e.nombre,e.estado,e.puntaje_total,a.nombre area FROM examenes e JOIN areas a ON a.id_area=e.id_area ORDER BY e.id_examen DESC')).mappings().all()
            actual = next((x for x in examenes if x['id_examen'] == examen), None)
            preguntas = c.execute(text("""SELECT pv.id_version,pv.enunciado,p.id_pregunta,p.id_examen_destino,m.id_materia,m.nombre materia,et.nombre eje
                FROM examenes ex JOIN pregunta_areas pa ON pa.id_area=ex.id_area JOIN preguntas p ON p.id_pregunta=pa.id_pregunta AND p.estado='APROBADA'
                JOIN pregunta_versiones pv ON pv.id_pregunta=p.id_pregunta AND pv.estado='ACTIVA' AND pv.sellada=1
                JOIN materias m ON m.id_materia=p.id_materia JOIN ejes_tematicos et ON et.id_eje=m.id_eje
                WHERE ex.id_examen=:id ORDER BY et.nombre,m.nombre,p.id_pregunta"""), {'id': examen}).mappings().all() if actual else []
            versiones = c.execute(text('SELECT id_version,codigo_version FROM versiones_examen WHERE id_examen=:id ORDER BY codigo_version'), {'id': examen}).mappings().all() if actual else []
            claves = c.execute(text("""SELECT v.id_version,v.codigo_version,ep.numero_pregunta,ep.id_version_pregunta,pv.enunciado,COALESCE((SELECT pr.respuesta_correcta FROM plantilla_respuestas pr JOIN revisiones_clave rc ON rc.id_revision_clave=pr.id_revision_clave WHERE rc.id_version_examen=v.id_version AND rc.estado='CONFIRMADA' AND pr.numero_pregunta=ep.numero_pregunta ORDER BY rc.numero_revision DESC LIMIT 1),pv.respuesta_correcta) sugerida,
                (SELECT MAX(rc.numero_revision) FROM revisiones_clave rc WHERE rc.id_version_examen=v.id_version AND rc.estado='CONFIRMADA') revision
                FROM versiones_examen v JOIN examen_preguntas ep ON ep.id_version_examen=v.id_version
                JOIN pregunta_versiones pv ON pv.id_version=ep.id_version_pregunta WHERE v.id_examen=:id ORDER BY v.codigo_version,ep.numero_pregunta"""), {'id': examen}).mappings().all() if actual else []
            return examenes, actual, preguntas, versiones, claves

    def configurar(self, examen, ids, puntajes, versiones, penalizacion, usuario):
        with self.motor.begin() as c:
            ex = c.execute(text('SELECT estado,id_area,puntaje_total FROM examenes WHERE id_examen=:id FOR UPDATE'), {'id': examen}).mappings().first()
            if not ex:
                raise ValueError('El examen no existe.')
            tiene_versiones = c.execute(text('SELECT COUNT(*) FROM versiones_examen WHERE id_examen=:id'), {'id': examen}).scalar_one()
            Examen.validar_configuracion(ex['estado'], tiene_versiones)
            consulta = text("""SELECT pv.id_version,p.id_materia,m.id_eje FROM pregunta_versiones pv
                JOIN preguntas p ON p.id_pregunta=pv.id_pregunta JOIN materias m ON m.id_materia=p.id_materia
                JOIN pregunta_areas pa ON pa.id_pregunta=p.id_pregunta WHERE pv.id_version IN :ids
                AND pa.id_area=:area AND p.estado='APROBADA' AND pv.estado='ACTIVA' AND pv.sellada=1""").bindparams(bindparam('ids', expanding=True))
            elegidas = c.execute(consulta, {'ids': ids, 'area': ex['id_area']}).mappings().all()
            por_id, totales, pesos = ValidadorExamen.calcular_distribucion(ids, elegidas, puntajes, ex['puntaje_total'])
            for eje, peso in pesos.items():
                c.execute(text('INSERT INTO examen_ejes(id_examen,id_eje,peso_porcentaje) VALUES (:examen,:eje,:peso)'), {'examen': examen,'eje': eje,'peso': peso})
            for orden, (materia, cantidad) in enumerate(totales.items(), 1):
                c.execute(text('INSERT INTO distribucion_examen(id_examen,id_materia,orden,cantidad_preguntas,puntaje_por_pregunta) VALUES (:examen,:materia,:orden,:cantidad,:puntaje)'), {'examen': examen,'materia': materia,'orden': orden,'cantidad': cantidad,'puntaje': puntajes[materia]})
            for codigo in versiones:
                vid = c.execute(text('INSERT INTO versiones_examen(id_examen,codigo_version) VALUES (:examen,:codigo)'), {'examen': examen,'codigo': codigo}).lastrowid
                orden_ids = Examen.ordenar_versiones(ids, codigo)
                for numero, id in enumerate(orden_ids, 1):
                    c.execute(text('INSERT INTO examen_preguntas(id_version_examen,id_version_pregunta,numero_pregunta,puntaje) VALUES (:version,:pregunta,:numero,:puntaje)'), {'version': vid,'pregunta': id,'numero': numero,'puntaje': puntajes[por_id[id]['id_materia']]})
            c.execute(text("INSERT INTO configuracion_puntaje(id_examen,numero_revision,estado,creada_por,motivo,puntaje_incorrecta,usa_penalizacion) VALUES (:examen,1,'CONFIRMADA',:usuario,'Configuración inicial',:penalizacion,:usa)"), {'examen': examen,'usuario': usuario,'penalizacion': penalizacion,'usa': penalizacion < 0})
            c.execute(text("UPDATE examenes SET estado='APROBADO' WHERE id_examen=:id"), {'id': examen})
            c.execute(text("INSERT INTO historial_configuracion_examen(id_examen,usuario_modifico,descripcion_cambio) VALUES (:id,:usuario,'Configuración y aprobación inicial')"), {'id': examen,'usuario': usuario})

    def crear_clave(self, version, respuestas, motivo, usuario):
        with self.motor.begin() as c:
            v = c.execute(text("SELECT v.id_examen,e.estado FROM versiones_examen v JOIN examenes e ON e.id_examen=v.id_examen WHERE v.id_version=:id AND v.estado='ACTIVA' FOR UPDATE"), {'id': version}).mappings().first()
            if not v:
                raise ValueError('La versión no existe o está inactiva.')
            tiene_resultados = c.execute(text('SELECT COUNT(*) FROM resultados_examen WHERE id_examen=:id AND vigente=1'), {'id': v['id_examen']}).scalar_one()
            Examen.validar_revision_clave(v['estado'], tiene_resultados)
            filas = c.execute(text('SELECT numero_pregunta,id_version_pregunta FROM examen_preguntas WHERE id_version_examen=:id ORDER BY numero_pregunta'), {'id': version}).mappings().all()
            ValidadorExamen.validar_clave(respuestas, (x['numero_pregunta'] for x in filas))
            numero = c.execute(text('SELECT COALESCE(MAX(numero_revision),0)+1 FROM revisiones_clave WHERE id_version_examen=:id'), {'id': version}).scalar_one()
            revision = c.execute(text('INSERT INTO revisiones_clave(id_version_examen,numero_revision,creada_por,motivo) VALUES (:version,:numero,:usuario,:motivo)'), {'version': version,'numero': numero,'usuario': usuario,'motivo': motivo}).lastrowid
            for f in filas:
                c.execute(text('INSERT INTO plantilla_respuestas(id_revision_clave,id_version_examen,numero_pregunta,id_version_pregunta,respuesta_correcta) VALUES (:revision,:version,:numero,:pregunta,:respuesta)'), {'revision': revision,'version': version,'numero': f['numero_pregunta'],'pregunta': f['id_version_pregunta'],'respuesta': respuestas[f['numero_pregunta']]})
            c.execute(text("UPDATE revisiones_clave SET estado='CONFIRMADA' WHERE id_revision_clave=:id"), {'id': revision})

"""Cálculo inicial transaccional de resultados de cartillas validadas."""
from sqlalchemy import text
from dominio.evaluacion.calificador_resultados import calificar


class CalculoResultadosRepositorio:
    def __init__(self, motor):
        self.motor = motor

    def calcular(self, examen, usuario):
        with self.motor.begin() as c:
            ex = c.execute(text('SELECT estado FROM examenes WHERE id_examen=:id FOR UPDATE'), {'id': examen}).scalar_one_or_none()
            if ex not in ('APROBADO','APLICADO','CERRADO'):
                raise ValueError('El examen debe estar aprobado.')
            config = c.execute(text("SELECT id_configuracion,puntaje_incorrecta FROM configuracion_puntaje WHERE id_examen=:id AND estado='CONFIRMADA' ORDER BY numero_revision DESC LIMIT 1"), {'id': examen}).mappings().first()
            if not config:
                raise ValueError('Falta una política de puntaje confirmada.')
            cartillas = c.execute(text("SELECT id_cartilla,id_estudiante,id_version FROM cartillas WHERE id_examen=:id AND vigente=1 AND estado='VALIDADA' FOR UPDATE"), {'id': examen}).mappings().all()
            if not cartillas:
                raise ValueError('No hay cartillas vigentes validadas.')
            creados = 0
            for cartilla in cartillas:
                if c.execute(text('SELECT COUNT(*) FROM resultados_examen WHERE id_cartilla=:id AND vigente=1'), {'id': cartilla['id_cartilla']}).scalar_one():
                    continue
                clave = c.execute(text("SELECT id_revision_clave FROM revisiones_clave WHERE id_version_examen=:id AND estado='CONFIRMADA' ORDER BY numero_revision DESC LIMIT 1"), {'id': cartilla['id_version']}).scalar_one_or_none()
                proceso = c.execute(text("SELECT id_procesamiento FROM procesamiento_cartilla WHERE id_cartilla=:id AND resultado='EXITOSO' ORDER BY numero_intento DESC LIMIT 1"), {'id': cartilla['id_cartilla']}).scalar_one_or_none()
                if not clave or not proceso:
                    raise ValueError('Todas las cartillas necesitan una clave confirmada y lectura validada.')
                filas = c.execute(text("""SELECT ep.id_examen_pregunta,ep.id_version_pregunta,ep.puntaje,p.id_materia,rd.id_respuesta_detectada,rd.respuesta_detectada lectura,
                    cm.id_correccion,cm.resolucion,cm.respuesta_nueva corregida,pr.respuesta_correcta clave
                    FROM examen_preguntas ep JOIN pregunta_versiones pv ON pv.id_version=ep.id_version_pregunta
                    JOIN preguntas p ON p.id_pregunta=pv.id_pregunta JOIN plantilla_respuestas pr ON pr.id_revision_clave=:clave AND pr.numero_pregunta=ep.numero_pregunta
                    JOIN respuestas_detectadas rd ON rd.id_procesamiento=:proceso AND rd.numero_pregunta=ep.numero_pregunta
                    LEFT JOIN correcciones_manual cm ON cm.id_correccion=(SELECT MAX(x.id_correccion) FROM correcciones_manual x WHERE x.id_respuesta_detectada=rd.id_respuesta_detectada)
                    WHERE ep.id_version_examen=:version ORDER BY ep.numero_pregunta"""), {'clave': clave,'proceso': proceso,'version': cartilla['id_version']}).mappings().all()
                cantidad = c.execute(text('SELECT COUNT(*) FROM examen_preguntas WHERE id_version_examen=:version'), {'version': cartilla['id_version']}).scalar_one()
                if not cantidad or len(filas) != cantidad:
                    raise ValueError('La clave o las lecturas no cubren todas las preguntas.')
                detalles, materias, buenas, malas, blancas, puntaje = calificar(filas, config['puntaje_incorrecta'])
                numero = c.execute(text('SELECT COALESCE(MAX(numero_calculo),0)+1 FROM resultados_examen WHERE id_estudiante=:estudiante AND id_examen=:examen'), {'estudiante': cartilla['id_estudiante'],'examen': examen}).scalar_one()
                params = {'clave': clave,'config': config['id_configuracion'],'usuario': usuario,'estudiante': cartilla['id_estudiante'],'examen': examen,'version': cartilla['id_version'],'cartilla': cartilla['id_cartilla'],'proceso': proceso,'buenas': buenas,'malas': malas,'blancas': blancas,'puntaje': puntaje,'numero': numero}
                resultado = c.execute(text("""INSERT INTO resultados_examen(id_revision_clave,id_configuracion,calculado_por,id_estudiante,id_examen,id_version,id_cartilla,id_procesamiento,respuestas_correctas,respuestas_incorrectas,respuestas_blanco,puntaje_obtenido,numero_calculo) VALUES (:clave,:config,:usuario,:estudiante,:examen,:version,:cartilla,:proceso,:buenas,:malas,:blancas,:puntaje,:numero)"""), params).lastrowid
                for d in detalles:
                    c.execute(text("""INSERT INTO detalle_resultado(id_resultado,id_examen_pregunta,id_version_examen,id_version_pregunta,id_respuesta_detectada,id_correccion_aplicada,tipo_respuesta,respuesta_marcada,respuesta_correcta,es_correcta,puntaje_obtenido) VALUES (:resultado,:pregunta,:version,:version_pregunta,:lectura,:correccion,:tipo,:marcada,:correcta,:es_correcta,:puntaje)"""), {'resultado': resultado,'pregunta': d['id_examen_pregunta'],'version': cartilla['id_version'],'version_pregunta': d['id_version_pregunta'],'lectura': d['id_respuesta_detectada'],'correccion': d['id_correccion'],'tipo': d['tipo'],'marcada': d['marcada'],'correcta': d['clave'],'es_correcta': d['correcta'],'puntaje': d['obtenido']})
                for materia, m in materias.items():
                    c.execute(text('INSERT INTO resultado_materia(id_resultado,id_materia,preguntas_total,correctas,incorrectas,blanco,puntaje) VALUES (:resultado,:materia,:total,:correctas,:incorrectas,:blancos,:puntaje)'), dict(m, resultado=resultado, materia=materia))
                creados += 1
            return creados

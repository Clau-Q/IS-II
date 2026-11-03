from sqlalchemy import text


class PanelPendientesRepositorio:
    def __init__(self, motor):
        self.motor = motor

    def consultar(self):
        with self.motor.connect() as conexion:
            return conexion.execute(text("""SELECT
                (SELECT COUNT(*) FROM preguntas WHERE estado='REVISION') AS preguntas,
                (SELECT COUNT(*) FROM respuestas_detectadas r
                    JOIN cartillas c ON c.id_cartilla=r.id_cartilla
                    JOIN examen_preguntas ep ON ep.id_version_examen=c.id_version AND ep.numero_pregunta=r.numero_pregunta
                    WHERE c.vigente=1 AND c.estado NOT IN ('VALIDADA','ANULADA')
                    AND r.id_procesamiento=(SELECT MAX(pc.id_procesamiento) FROM procesamiento_cartilla pc WHERE pc.id_cartilla=c.id_cartilla)
                    AND r.requiere_revision=1
                    AND NOT EXISTS (SELECT 1 FROM correcciones_manual cm WHERE cm.id_respuesta_detectada=r.id_respuesta_detectada)) AS lecturas,
                (SELECT COUNT(*) FROM resultados_examen WHERE estado='CALCULADO' AND vigente=1) AS calculos,
                (SELECT COUNT(*) FROM resultados_examen WHERE estado='REVISADO' AND vigente=1) AS publicaciones""")).mappings().one()

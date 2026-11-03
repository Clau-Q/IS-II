-- Cartilla fisica de 90 posiciones; solo se evaluan las preguntas configuradas.
DELIMITER $$
DROP TRIGGER IF EXISTS trg_resultado_insert$$
CREATE TRIGGER trg_resultado_insert
BEFORE INSERT ON resultados_examen FOR EACH ROW
BEGIN
    IF NEW.estado <> 'CALCULADO' OR NOT EXISTS
      (SELECT 1 FROM revisiones_clave WHERE id_revision_clave = NEW.id_revision_clave AND estado = 'CONFIRMADA')
      OR NOT EXISTS (SELECT 1 FROM configuracion_puntaje WHERE id_configuracion = NEW.id_configuracion AND estado = 'CONFIRMADA')
      OR NOT EXISTS (SELECT 1 FROM cartillas WHERE id_cartilla = NEW.id_cartilla AND vigente = 1 AND estado = 'VALIDADA') THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Calcular requiere cartilla vigente validada, clave y politica confirmadas';
    END IF;
    -- Conservar las 90 posiciones leidas; evaluar solo las preguntas del examen.
    IF EXISTS (SELECT 1 FROM respuestas_detectadas rd
        INNER JOIN examen_preguntas ep ON ep.id_version_examen = NEW.id_version AND ep.numero_pregunta = rd.numero_pregunta
        WHERE rd.id_procesamiento = NEW.id_procesamiento
        AND rd.requiere_revision = 1 AND NOT EXISTS
          (SELECT 1 FROM correcciones_manual cm WHERE cm.id_respuesta_detectada = rd.id_respuesta_detectada))
      OR (SELECT COUNT(*) FROM respuestas_detectadas rd
          INNER JOIN examen_preguntas ep ON ep.id_version_examen = NEW.id_version AND ep.numero_pregunta = rd.numero_pregunta
          WHERE rd.id_procesamiento = NEW.id_procesamiento)
        <> (SELECT COUNT(*) FROM examen_preguntas WHERE id_version_examen = NEW.id_version)
      OR NOT EXISTS (SELECT 1 FROM procesamiento_cartilla WHERE id_procesamiento = NEW.id_procesamiento AND resultado = 'EXITOSO') THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La lectura debe estar completa y todas las dudas resueltas';
    END IF;
    IF NEW.puntaje_obtenido < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El puntaje final no puede ser negativo';
    END IF;
END$$
DELIMITER ;

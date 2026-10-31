USE sistema_evaluacion;
UPDATE roles SET descripcion='Administrador principal y acceso institucional' WHERE nombre='DIRECTOR';
INSERT IGNORE INTO rol_permisos(id_rol,id_permiso) SELECT d.id_rol,rp.id_permiso FROM roles d JOIN roles c ON c.nombre='COORDINADOR' JOIN rol_permisos rp ON rp.id_rol=c.id_rol WHERE d.nombre='DIRECTOR';
DELIMITER $$
DROP TRIGGER IF EXISTS trg_fecha_aprobacion_pregunta$$
CREATE TRIGGER trg_fecha_aprobacion_pregunta
BEFORE UPDATE ON preguntas
FOR EACH ROW
BEGIN
DECLARE v_areas INT;
IF NEW.estado='APROBADA'
AND OLD.estado <> 'APROBADA'
THEN
IF NEW.aprobado_por IS NULL THEN
SIGNAL SQLSTATE '45000'
SET MESSAGE_TEXT = 'Se requiere el usuario que aprueba la pregunta';
END IF;
SELECT COUNT(*) INTO v_areas
FROM pregunta_areas
WHERE id_pregunta = NEW.id_pregunta;
IF v_areas = 0 THEN
SIGNAL SQLSTATE '45000'
SET MESSAGE_TEXT = 'La pregunta debe tener al menos un area para ser aprobada';
END IF;
IF OLD.estado <> 'REVISION' OR NOT EXISTS
  (SELECT 1 FROM pregunta_versiones WHERE id_pregunta = NEW.id_pregunta AND estado = 'ACTIVA' AND sellada = 1) THEN
SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Aprobar requiere revision y version activa sellada';
END IF;
IF NOT EXISTS (SELECT 1 FROM usuario_roles ur INNER JOIN roles ro ON ro.id_rol = ur.id_rol
  WHERE ur.id_usuario = NEW.aprobado_por AND ro.nombre IN ('COORDINADOR','DIRECTOR')) THEN
SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La aprobacion requiere rol COORDINADOR o DIRECTOR; puede ser el autor';
END IF;
SET NEW.fecha_aprobacion = NOW();
END IF;
END$$
DROP PROCEDURE IF EXISTS sp_registrar_cartilla$$
CREATE PROCEDURE sp_registrar_cartilla(
    IN p_estudiante INT, IN p_examen INT, IN p_version INT,
    IN p_archivo VARCHAR(255), IN p_usuario INT, IN p_motivo TEXT)
BEGIN
    DECLARE v_simulacro INT;
    DECLARE v_participacion INT;
    DECLARE v_examen INT;
    DECLARE v_anterior INT;
    DECLARE v_numero INT;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK; RESIGNAL; END;
    START TRANSACTION;
    SELECT id_simulacro INTO v_simulacro FROM examenes WHERE id_examen = p_examen FOR UPDATE;
    IF NOT EXISTS (SELECT 1 FROM usuario_roles ur INNER JOIN roles ro ON ro.id_rol = ur.id_rol
      INNER JOIN usuarios u ON u.id_usuario = ur.id_usuario
      WHERE ur.id_usuario = p_usuario AND ro.nombre IN ('COORDINADOR','DIRECTOR') AND u.estado = 'ACTIVO') THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Se requiere coordinador o director activo';
    END IF;
    INSERT INTO participaciones(id_estudiante, id_simulacro, id_examen)
    VALUES(p_estudiante, v_simulacro, p_examen)
    ON DUPLICATE KEY UPDATE id_participacion = LAST_INSERT_ID(id_participacion);
    SELECT id_participacion, id_examen INTO v_participacion, v_examen
    FROM participaciones WHERE id_estudiante = p_estudiante AND id_simulacro = v_simulacro FOR UPDATE;
    IF v_examen <> p_examen THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El estudiante ya participa en otra area del simulacro';
    END IF;
    SELECT MAX(id_cartilla), COALESCE(MAX(numero_recepcion), 0) + 1 INTO v_anterior, v_numero
    FROM cartillas WHERE id_participacion = v_participacion;
    IF v_anterior IS NOT NULL AND (p_motivo IS NULL OR CHAR_LENGTH(TRIM(p_motivo)) = 0) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El reemplazo necesita motivo';
    END IF;
    UPDATE cartillas SET vigente = 0 WHERE id_participacion = v_participacion AND vigente = 1;
    INSERT INTO cartillas(id_participacion, numero_recepcion, reemplaza_cartilla, motivo_reemplazo,
        id_estudiante, id_examen, id_version, archivo_imagen, fecha_recepcion, operador_recepcion)
    VALUES(v_participacion, v_numero, v_anterior, p_motivo, p_estudiante, p_examen, p_version, p_archivo, CURRENT_DATE, p_usuario);
    COMMIT;
END$$
DROP PROCEDURE IF EXISTS sp_publicar_examen$$
CREATE PROCEDURE sp_publicar_examen(IN p_examen INT, IN p_usuario INT)
BEGIN
    DECLARE v_examen INT;
    DECLARE v_numero INT;
    DECLARE v_publicacion INT;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK; RESIGNAL; END;
    START TRANSACTION;
    SELECT id_examen INTO v_examen FROM examenes WHERE id_examen = p_examen FOR UPDATE;
    IF NOT EXISTS (SELECT 1 FROM usuario_roles ur INNER JOIN roles ro ON ro.id_rol = ur.id_rol
      INNER JOIN usuarios u ON u.id_usuario = ur.id_usuario
      WHERE ur.id_usuario = p_usuario AND ro.nombre IN ('COORDINADOR','DIRECTOR') AND u.estado = 'ACTIVO') THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Se requiere coordinador o director activo';
    END IF;
    IF NOT EXISTS (SELECT 1 FROM cartillas WHERE id_examen = p_examen AND vigente = 1)
      OR EXISTS (SELECT 1 FROM cartillas c WHERE c.id_examen = p_examen AND c.vigente = 1
        AND (c.estado <> 'VALIDADA' OR NOT EXISTS (SELECT 1 FROM resultados_examen r
          WHERE r.id_cartilla = c.id_cartilla AND r.vigente = 1 AND r.estado IN ('REVISADO','PUBLICADO')))) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Todas las cartillas vigentes requieren resultado validado';
    END IF;
    SELECT COALESCE(MAX(numero_publicacion), 0) + 1 INTO v_numero FROM publicaciones_examen WHERE id_examen = p_examen;
    UPDATE publicaciones_examen SET vigente = 0 WHERE id_examen = p_examen AND vigente = 1;
    UPDATE resultados_examen SET estado = 'PUBLICADO' WHERE id_examen = p_examen AND vigente = 1 AND estado = 'REVISADO';
    INSERT INTO publicaciones_examen(id_examen, numero_publicacion, publicada_por) VALUES(p_examen, v_numero, p_usuario);
    SET v_publicacion = LAST_INSERT_ID();
    INSERT INTO publicacion_resultados(id_publicacion, id_examen, id_resultado, posicion)
    SELECT v_publicacion, p_examen, r.id_resultado,
        RANK() OVER (ORDER BY r.puntaje_obtenido DESC)
    FROM resultados_examen r INNER JOIN cartillas c ON c.id_cartilla = r.id_cartilla
    WHERE r.id_examen = p_examen AND r.vigente = 1 AND r.estado = 'PUBLICADO' AND c.vigente = 1;
    COMMIT;
END$$
DELIMITER ;

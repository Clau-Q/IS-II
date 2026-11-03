-- Datos iniciales del sistema académico.
-- Ejecutar después de nueva_base_de_datos.sql en MySQL 8.0.
-- Conserva los registros existentes y permite repetir la carga.
-- Incluye áreas, materias, estudiantes, docente y 80 preguntas por área.
-- La cantidad corresponde a la distribución; no inserta enunciados ni resultados.
-- Las 30 fotos JPEG se conservan en cartillas/ para cargarlas desde el sistema.
USE sistema_evaluacion;
SET NAMES utf8mb4;

DELIMITER $$
CREATE PROCEDURE sp_cargar_datos_iniciales_academicos()
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
    START TRANSACTION;

    -- Áreas académicas.
    INSERT INTO areas (codigo, nombre, descripcion, estado)
    SELECT 'ING', 'Ingenierías', 'Área orientada a carreras de ingeniería', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM areas WHERE codigo = 'ING');
    SET @area_1 = (SELECT MIN(id_area) FROM areas WHERE codigo = 'ING');
    INSERT INTO areas (codigo, nombre, descripcion, estado)
    SELECT 'BIO', 'Biomédicas', 'Área ciencias de la salud', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM areas WHERE codigo = 'BIO');
    SET @area_2 = (SELECT MIN(id_area) FROM areas WHERE codigo = 'BIO');
    INSERT INTO areas (codigo, nombre, descripcion, estado)
    SELECT 'SOC', 'Sociales', 'Área ciencias sociales', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM areas WHERE codigo = 'SOC');
    SET @area_3 = (SELECT MIN(id_area) FROM areas WHERE codigo = 'SOC');

    -- Ejes temáticos y materias.
    INSERT INTO ejes_tematicos (nombre, descripcion, estado)
    SELECT 'Matemática', 'Área matemática', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM ejes_tematicos WHERE nombre = 'Matemática');
    SET @eje_1 = (SELECT MIN(id_eje) FROM ejes_tematicos WHERE nombre = 'Matemática');
    INSERT INTO ejes_tematicos (nombre, descripcion, estado)
    SELECT 'Comunicación', 'Lenguaje y comprensión lectora', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM ejes_tematicos WHERE nombre = 'Comunicación');
    SET @eje_2 = (SELECT MIN(id_eje) FROM ejes_tematicos WHERE nombre = 'Comunicación');
    INSERT INTO ejes_tematicos (nombre, descripcion, estado)
    SELECT 'Aptitud Académica', NULL, 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM ejes_tematicos WHERE nombre = 'Aptitud Académica');
    SET @eje_5 = (SELECT MIN(id_eje) FROM ejes_tematicos WHERE nombre = 'Aptitud Académica');
    INSERT INTO ejes_tematicos (nombre, descripcion, estado)
    SELECT 'Ciencias Sociales', NULL, 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM ejes_tematicos WHERE nombre = 'Ciencias Sociales');
    SET @eje_6 = (SELECT MIN(id_eje) FROM ejes_tematicos WHERE nombre = 'Ciencias Sociales');
    INSERT INTO ejes_tematicos (nombre, descripcion, estado)
    SELECT 'Ciencia y Tecnología', NULL, 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM ejes_tematicos WHERE nombre = 'Ciencia y Tecnología');
    SET @eje_7 = (SELECT MIN(id_eje) FROM ejes_tematicos WHERE nombre = 'Ciencia y Tecnología');
    INSERT INTO ejes_tematicos (nombre, descripcion, estado)
    SELECT 'Persona y Familia', NULL, 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM ejes_tematicos WHERE nombre = 'Persona y Familia');
    SET @eje_8 = (SELECT MIN(id_eje) FROM ejes_tematicos WHERE nombre = 'Persona y Familia');
    INSERT INTO ejes_tematicos (nombre, descripcion, estado)
    SELECT 'Idioma Extranjero/Lengua Originaria', NULL, 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM ejes_tematicos WHERE nombre = 'Idioma Extranjero/Lengua Originaria');
    SET @eje_9 = (SELECT MIN(id_eje) FROM ejes_tematicos WHERE nombre = 'Idioma Extranjero/Lengua Originaria');
    INSERT INTO materias (id_eje, codigo, nombre, descripcion, valor_referencia, estado)
    SELECT @eje_5, NULL, 'Razonamiento Lógico', NULL, NULL, 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM materias WHERE nombre = 'Razonamiento Lógico' AND id_eje = @eje_5);
    SET @materia_2 = (SELECT MIN(id_materia) FROM materias WHERE nombre = 'Razonamiento Lógico' AND id_eje = @eje_5);
    INSERT INTO materias (id_eje, codigo, nombre, descripcion, valor_referencia, estado)
    SELECT @eje_5, NULL, 'Razonamiento Matemático', NULL, NULL, 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM materias WHERE nombre = 'Razonamiento Matemático' AND id_eje = @eje_5);
    SET @materia_3 = (SELECT MIN(id_materia) FROM materias WHERE nombre = 'Razonamiento Matemático' AND id_eje = @eje_5);
    INSERT INTO materias (id_eje, codigo, nombre, descripcion, valor_referencia, estado)
    SELECT @eje_5, NULL, 'Razonamiento Verbal', NULL, NULL, 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM materias WHERE nombre = 'Razonamiento Verbal' AND id_eje = @eje_5);
    SET @materia_4 = (SELECT MIN(id_materia) FROM materias WHERE nombre = 'Razonamiento Verbal' AND id_eje = @eje_5);
    INSERT INTO materias (id_eje, codigo, nombre, descripcion, valor_referencia, estado)
    SELECT @eje_5, NULL, 'Comprensión Lectora', NULL, NULL, 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM materias WHERE nombre = 'Comprensión Lectora' AND id_eje = @eje_5);
    SET @materia_5 = (SELECT MIN(id_materia) FROM materias WHERE nombre = 'Comprensión Lectora' AND id_eje = @eje_5);
    INSERT INTO materias (id_eje, codigo, nombre, descripcion, valor_referencia, estado)
    SELECT @eje_1, NULL, 'Álgebra', NULL, NULL, 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM materias WHERE nombre = 'Álgebra' AND id_eje = @eje_1);
    SET @materia_6 = (SELECT MIN(id_materia) FROM materias WHERE nombre = 'Álgebra' AND id_eje = @eje_1);
    INSERT INTO materias (id_eje, codigo, nombre, descripcion, valor_referencia, estado)
    SELECT @eje_1, NULL, 'Aritmética', NULL, NULL, 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM materias WHERE nombre = 'Aritmética' AND id_eje = @eje_1);
    SET @materia_7 = (SELECT MIN(id_materia) FROM materias WHERE nombre = 'Aritmética' AND id_eje = @eje_1);
    INSERT INTO materias (id_eje, codigo, nombre, descripcion, valor_referencia, estado)
    SELECT @eje_1, NULL, 'Geometría', NULL, NULL, 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM materias WHERE nombre = 'Geometría' AND id_eje = @eje_1);
    SET @materia_8 = (SELECT MIN(id_materia) FROM materias WHERE nombre = 'Geometría' AND id_eje = @eje_1);
    INSERT INTO materias (id_eje, codigo, nombre, descripcion, valor_referencia, estado)
    SELECT @eje_1, NULL, 'Trigonometría', NULL, NULL, 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM materias WHERE nombre = 'Trigonometría' AND id_eje = @eje_1);
    SET @materia_9 = (SELECT MIN(id_materia) FROM materias WHERE nombre = 'Trigonometría' AND id_eje = @eje_1);
    INSERT INTO materias (id_eje, codigo, nombre, descripcion, valor_referencia, estado)
    SELECT @eje_6, NULL, 'Historia', NULL, NULL, 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM materias WHERE nombre = 'Historia' AND id_eje = @eje_6);
    SET @materia_10 = (SELECT MIN(id_materia) FROM materias WHERE nombre = 'Historia' AND id_eje = @eje_6);
    INSERT INTO materias (id_eje, codigo, nombre, descripcion, valor_referencia, estado)
    SELECT @eje_6, NULL, 'Geografía', NULL, NULL, 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM materias WHERE nombre = 'Geografía' AND id_eje = @eje_6);
    SET @materia_11 = (SELECT MIN(id_materia) FROM materias WHERE nombre = 'Geografía' AND id_eje = @eje_6);
    INSERT INTO materias (id_eje, codigo, nombre, descripcion, valor_referencia, estado)
    SELECT @eje_7, NULL, 'Química', NULL, NULL, 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM materias WHERE nombre = 'Química' AND id_eje = @eje_7);
    SET @materia_12 = (SELECT MIN(id_materia) FROM materias WHERE nombre = 'Química' AND id_eje = @eje_7);
    INSERT INTO materias (id_eje, codigo, nombre, descripcion, valor_referencia, estado)
    SELECT @eje_7, NULL, 'Biología', NULL, NULL, 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM materias WHERE nombre = 'Biología' AND id_eje = @eje_7);
    SET @materia_13 = (SELECT MIN(id_materia) FROM materias WHERE nombre = 'Biología' AND id_eje = @eje_7);
    INSERT INTO materias (id_eje, codigo, nombre, descripcion, valor_referencia, estado)
    SELECT @eje_7, NULL, 'Física', NULL, NULL, 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM materias WHERE nombre = 'Física' AND id_eje = @eje_7);
    SET @materia_14 = (SELECT MIN(id_materia) FROM materias WHERE nombre = 'Física' AND id_eje = @eje_7);
    INSERT INTO materias (id_eje, codigo, nombre, descripcion, valor_referencia, estado)
    SELECT @eje_8, NULL, 'Filosofía', NULL, NULL, 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM materias WHERE nombre = 'Filosofía' AND id_eje = @eje_8);
    SET @materia_15 = (SELECT MIN(id_materia) FROM materias WHERE nombre = 'Filosofía' AND id_eje = @eje_8);
    INSERT INTO materias (id_eje, codigo, nombre, descripcion, valor_referencia, estado)
    SELECT @eje_8, NULL, 'Psicología', NULL, NULL, 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM materias WHERE nombre = 'Psicología' AND id_eje = @eje_8);
    SET @materia_16 = (SELECT MIN(id_materia) FROM materias WHERE nombre = 'Psicología' AND id_eje = @eje_8);
    INSERT INTO materias (id_eje, codigo, nombre, descripcion, valor_referencia, estado)
    SELECT @eje_8, NULL, 'Educación Cívica', NULL, NULL, 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM materias WHERE nombre = 'Educación Cívica' AND id_eje = @eje_8);
    SET @materia_17 = (SELECT MIN(id_materia) FROM materias WHERE nombre = 'Educación Cívica' AND id_eje = @eje_8);
    INSERT INTO materias (id_eje, codigo, nombre, descripcion, valor_referencia, estado)
    SELECT @eje_2, NULL, 'Lenguaje', NULL, NULL, 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM materias WHERE nombre = 'Lenguaje' AND id_eje = @eje_2);
    SET @materia_18 = (SELECT MIN(id_materia) FROM materias WHERE nombre = 'Lenguaje' AND id_eje = @eje_2);
    INSERT INTO materias (id_eje, codigo, nombre, descripcion, valor_referencia, estado)
    SELECT @eje_2, NULL, 'Literatura', NULL, NULL, 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM materias WHERE nombre = 'Literatura' AND id_eje = @eje_2);
    SET @materia_19 = (SELECT MIN(id_materia) FROM materias WHERE nombre = 'Literatura' AND id_eje = @eje_2);
    INSERT INTO materias (id_eje, codigo, nombre, descripcion, valor_referencia, estado)
    SELECT @eje_9, NULL, 'Lectura', NULL, NULL, 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM materias WHERE nombre = 'Lectura' AND id_eje = @eje_9);
    SET @materia_20 = (SELECT MIN(id_materia) FROM materias WHERE nombre = 'Lectura' AND id_eje = @eje_9);
    INSERT INTO materias (id_eje, codigo, nombre, descripcion, valor_referencia, estado)
    SELECT @eje_9, NULL, 'Gramática', NULL, NULL, 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM materias WHERE nombre = 'Gramática' AND id_eje = @eje_9);
    SET @materia_21 = (SELECT MIN(id_materia) FROM materias WHERE nombre = 'Gramática' AND id_eje = @eje_9);

    -- Docente y asignación de materias.
    INSERT INTO usuarios (username, password_hash, nombres, apellidos, estado)
    SELECT 'docente', 'pbkdf2:sha256:1000000$y1UnncYou9CBqWpc$63fa4c1940efbcf4de3c4fc7f259b601bce3c07a63be31a043ffd37064d523e9', 'Docente', 'Académico', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM usuarios WHERE username = 'docente');
    SET @usuario_docente = (SELECT MIN(id_usuario) FROM usuarios WHERE username = 'docente');
    SET @rol_docente = (SELECT MIN(id_rol) FROM roles WHERE nombre = 'DOCENTE');
    INSERT INTO usuario_roles (id_usuario, id_rol)
    SELECT @usuario_docente, @rol_docente WHERE NOT EXISTS (SELECT 1 FROM usuario_roles WHERE id_usuario = @usuario_docente AND id_rol = @rol_docente);
    INSERT INTO docentes (id_usuario, codigo_docente, especialidad)
    SELECT @usuario_docente, 'DOC-001', 'Formación académica' WHERE NOT EXISTS (SELECT 1 FROM docentes WHERE id_usuario = @usuario_docente);
    SET @docente = (SELECT MIN(id_docente) FROM docentes WHERE id_usuario = @usuario_docente);
    INSERT INTO docente_materias (id_docente, id_materia, fecha_asignacion, estado)
    SELECT @docente, @materia_2, '2026-01-01', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM docente_materias WHERE id_docente = @docente AND id_materia = @materia_2);
    INSERT INTO docente_materias (id_docente, id_materia, fecha_asignacion, estado)
    SELECT @docente, @materia_3, '2026-01-01', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM docente_materias WHERE id_docente = @docente AND id_materia = @materia_3);
    INSERT INTO docente_materias (id_docente, id_materia, fecha_asignacion, estado)
    SELECT @docente, @materia_4, '2026-01-01', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM docente_materias WHERE id_docente = @docente AND id_materia = @materia_4);
    INSERT INTO docente_materias (id_docente, id_materia, fecha_asignacion, estado)
    SELECT @docente, @materia_5, '2026-01-01', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM docente_materias WHERE id_docente = @docente AND id_materia = @materia_5);
    INSERT INTO docente_materias (id_docente, id_materia, fecha_asignacion, estado)
    SELECT @docente, @materia_6, '2026-01-01', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM docente_materias WHERE id_docente = @docente AND id_materia = @materia_6);
    INSERT INTO docente_materias (id_docente, id_materia, fecha_asignacion, estado)
    SELECT @docente, @materia_7, '2026-01-01', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM docente_materias WHERE id_docente = @docente AND id_materia = @materia_7);
    INSERT INTO docente_materias (id_docente, id_materia, fecha_asignacion, estado)
    SELECT @docente, @materia_8, '2026-01-01', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM docente_materias WHERE id_docente = @docente AND id_materia = @materia_8);
    INSERT INTO docente_materias (id_docente, id_materia, fecha_asignacion, estado)
    SELECT @docente, @materia_9, '2026-01-01', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM docente_materias WHERE id_docente = @docente AND id_materia = @materia_9);
    INSERT INTO docente_materias (id_docente, id_materia, fecha_asignacion, estado)
    SELECT @docente, @materia_10, '2026-01-01', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM docente_materias WHERE id_docente = @docente AND id_materia = @materia_10);
    INSERT INTO docente_materias (id_docente, id_materia, fecha_asignacion, estado)
    SELECT @docente, @materia_11, '2026-01-01', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM docente_materias WHERE id_docente = @docente AND id_materia = @materia_11);
    INSERT INTO docente_materias (id_docente, id_materia, fecha_asignacion, estado)
    SELECT @docente, @materia_12, '2026-01-01', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM docente_materias WHERE id_docente = @docente AND id_materia = @materia_12);
    INSERT INTO docente_materias (id_docente, id_materia, fecha_asignacion, estado)
    SELECT @docente, @materia_13, '2026-01-01', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM docente_materias WHERE id_docente = @docente AND id_materia = @materia_13);
    INSERT INTO docente_materias (id_docente, id_materia, fecha_asignacion, estado)
    SELECT @docente, @materia_14, '2026-01-01', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM docente_materias WHERE id_docente = @docente AND id_materia = @materia_14);
    INSERT INTO docente_materias (id_docente, id_materia, fecha_asignacion, estado)
    SELECT @docente, @materia_15, '2026-01-01', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM docente_materias WHERE id_docente = @docente AND id_materia = @materia_15);
    INSERT INTO docente_materias (id_docente, id_materia, fecha_asignacion, estado)
    SELECT @docente, @materia_16, '2026-01-01', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM docente_materias WHERE id_docente = @docente AND id_materia = @materia_16);
    INSERT INTO docente_materias (id_docente, id_materia, fecha_asignacion, estado)
    SELECT @docente, @materia_17, '2026-01-01', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM docente_materias WHERE id_docente = @docente AND id_materia = @materia_17);
    INSERT INTO docente_materias (id_docente, id_materia, fecha_asignacion, estado)
    SELECT @docente, @materia_18, '2026-01-01', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM docente_materias WHERE id_docente = @docente AND id_materia = @materia_18);
    INSERT INTO docente_materias (id_docente, id_materia, fecha_asignacion, estado)
    SELECT @docente, @materia_19, '2026-01-01', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM docente_materias WHERE id_docente = @docente AND id_materia = @materia_19);
    INSERT INTO docente_materias (id_docente, id_materia, fecha_asignacion, estado)
    SELECT @docente, @materia_20, '2026-01-01', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM docente_materias WHERE id_docente = @docente AND id_materia = @materia_20);
    INSERT INTO docente_materias (id_docente, id_materia, fecha_asignacion, estado)
    SELECT @docente, @materia_21, '2026-01-01', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM docente_materias WHERE id_docente = @docente AND id_materia = @materia_21);

    -- Estudiantes y su área académica.
    INSERT INTO estudiantes (codigo_estudiante, dni, nombres, apellidos, fecha_nacimiento, telefono, carrera_interes, estado)
    SELECT 'EST-78354712', '78354712', 'Carlos', 'García López', NULL, '98354712', 'Ingeniería Industrial', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM estudiantes WHERE dni = '78354712' OR codigo_estudiante = 'EST-78354712');
    SET @estudiante_3 = (SELECT MIN(id_estudiante) FROM estudiantes WHERE dni = '78354712' OR codigo_estudiante = 'EST-78354712');
    INSERT INTO estudiante_area_historial (id_estudiante, id_area, fecha_inicio)
    SELECT @estudiante_3, @area_1, '2026-11-01' WHERE NOT EXISTS (SELECT 1 FROM estudiante_area_historial WHERE id_estudiante = @estudiante_3 AND fecha_fin IS NULL);
    INSERT INTO estudiantes (codigo_estudiante, dni, nombres, apellidos, fecha_nacimiento, telefono, carrera_interes, estado)
    SELECT 'EST-73118023', '73118023', 'Ana', 'Martínez Silva', NULL, '93118023', 'Ingeniería Mecánica', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM estudiantes WHERE dni = '73118023' OR codigo_estudiante = 'EST-73118023');
    SET @estudiante_4 = (SELECT MIN(id_estudiante) FROM estudiantes WHERE dni = '73118023' OR codigo_estudiante = 'EST-73118023');
    INSERT INTO estudiante_area_historial (id_estudiante, id_area, fecha_inicio)
    SELECT @estudiante_4, @area_1, '2026-11-01' WHERE NOT EXISTS (SELECT 1 FROM estudiante_area_historial WHERE id_estudiante = @estudiante_4 AND fecha_fin IS NULL);
    INSERT INTO estudiantes (codigo_estudiante, dni, nombres, apellidos, fecha_nacimiento, telefono, carrera_interes, estado)
    SELECT 'EST-74134508', '74134508', 'Luis', 'Rodríguez Pérez', NULL, '94134508', 'Ingeniería Eléctrica', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM estudiantes WHERE dni = '74134508' OR codigo_estudiante = 'EST-74134508');
    SET @estudiante_5 = (SELECT MIN(id_estudiante) FROM estudiantes WHERE dni = '74134508' OR codigo_estudiante = 'EST-74134508');
    INSERT INTO estudiante_area_historial (id_estudiante, id_area, fecha_inicio)
    SELECT @estudiante_5, @area_1, '2026-11-01' WHERE NOT EXISTS (SELECT 1 FROM estudiante_area_historial WHERE id_estudiante = @estudiante_5 AND fecha_fin IS NULL);
    INSERT INTO estudiantes (codigo_estudiante, dni, nombres, apellidos, fecha_nacimiento, telefono, carrera_interes, estado)
    SELECT 'EST-75959214', '75959214', 'María', 'Hernández Vega', NULL, '95959214', 'Ingeniería Electrónica', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM estudiantes WHERE dni = '75959214' OR codigo_estudiante = 'EST-75959214');
    SET @estudiante_6 = (SELECT MIN(id_estudiante) FROM estudiantes WHERE dni = '75959214' OR codigo_estudiante = 'EST-75959214');
    INSERT INTO estudiante_area_historial (id_estudiante, id_area, fecha_inicio)
    SELECT @estudiante_6, @area_1, '2026-11-01' WHERE NOT EXISTS (SELECT 1 FROM estudiante_area_historial WHERE id_estudiante = @estudiante_6 AND fecha_fin IS NULL);
    INSERT INTO estudiantes (codigo_estudiante, dni, nombres, apellidos, fecha_nacimiento, telefono, carrera_interes, estado)
    SELECT 'EST-74767647', '74767647', 'Jorge', 'Díaz Morales', NULL, '94767647', 'Ingeniería Química', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM estudiantes WHERE dni = '74767647' OR codigo_estudiante = 'EST-74767647');
    SET @estudiante_7 = (SELECT MIN(id_estudiante) FROM estudiantes WHERE dni = '74767647' OR codigo_estudiante = 'EST-74767647');
    INSERT INTO estudiante_area_historial (id_estudiante, id_area, fecha_inicio)
    SELECT @estudiante_7, @area_1, '2026-11-01' WHERE NOT EXISTS (SELECT 1 FROM estudiante_area_historial WHERE id_estudiante = @estudiante_7 AND fecha_fin IS NULL);
    INSERT INTO estudiantes (codigo_estudiante, dni, nombres, apellidos, fecha_nacimiento, telefono, carrera_interes, estado)
    SELECT 'EST-79617451', '79617451', 'Carmen', 'Flores Ruiz', NULL, '99617451', 'Ingeniería Ambiental', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM estudiantes WHERE dni = '79617451' OR codigo_estudiante = 'EST-79617451');
    SET @estudiante_8 = (SELECT MIN(id_estudiante) FROM estudiantes WHERE dni = '79617451' OR codigo_estudiante = 'EST-79617451');
    INSERT INTO estudiante_area_historial (id_estudiante, id_area, fecha_inicio)
    SELECT @estudiante_8, @area_1, '2026-11-01' WHERE NOT EXISTS (SELECT 1 FROM estudiante_area_historial WHERE id_estudiante = @estudiante_8 AND fecha_fin IS NULL);
    INSERT INTO estudiantes (codigo_estudiante, dni, nombres, apellidos, fecha_nacimiento, telefono, carrera_interes, estado)
    SELECT 'EST-71234567', '71234567', 'Roberto', 'Silva Torres', NULL, '91234567', 'Ingeniería de Sistemas', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM estudiantes WHERE dni = '71234567' OR codigo_estudiante = 'EST-71234567');
    SET @estudiante_9 = (SELECT MIN(id_estudiante) FROM estudiantes WHERE dni = '71234567' OR codigo_estudiante = 'EST-71234567');
    INSERT INTO estudiante_area_historial (id_estudiante, id_area, fecha_inicio)
    SELECT @estudiante_9, @area_1, '2026-11-01' WHERE NOT EXISTS (SELECT 1 FROM estudiante_area_historial WHERE id_estudiante = @estudiante_9 AND fecha_fin IS NULL);
    INSERT INTO estudiantes (codigo_estudiante, dni, nombres, apellidos, fecha_nacimiento, telefono, carrera_interes, estado)
    SELECT 'EST-77654321', '77654321', 'Paola', 'Mendoza Ruiz', NULL, '97654321', 'Ingeniería de Materiales', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM estudiantes WHERE dni = '77654321' OR codigo_estudiante = 'EST-77654321');
    SET @estudiante_10 = (SELECT MIN(id_estudiante) FROM estudiantes WHERE dni = '77654321' OR codigo_estudiante = 'EST-77654321');
    INSERT INTO estudiante_area_historial (id_estudiante, id_area, fecha_inicio)
    SELECT @estudiante_10, @area_1, '2026-11-01' WHERE NOT EXISTS (SELECT 1 FROM estudiante_area_historial WHERE id_estudiante = @estudiante_10 AND fecha_fin IS NULL);
    INSERT INTO estudiantes (codigo_estudiante, dni, nombres, apellidos, fecha_nacimiento, telefono, carrera_interes, estado)
    SELECT 'EST-73456789', '73456789', 'Gabriel', 'Rojas Castro', NULL, '93456789', 'Ingeniería Civil', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM estudiantes WHERE dni = '73456789' OR codigo_estudiante = 'EST-73456789');
    SET @estudiante_11 = (SELECT MIN(id_estudiante) FROM estudiantes WHERE dni = '73456789' OR codigo_estudiante = 'EST-73456789');
    INSERT INTO estudiante_area_historial (id_estudiante, id_area, fecha_inicio)
    SELECT @estudiante_11, @area_1, '2026-11-01' WHERE NOT EXISTS (SELECT 1 FROM estudiante_area_historial WHERE id_estudiante = @estudiante_11 AND fecha_fin IS NULL);
    INSERT INTO estudiantes (codigo_estudiante, dni, nombres, apellidos, fecha_nacimiento, telefono, carrera_interes, estado)
    SELECT 'EST-77889900', '77889900', 'Natalia', 'Paredes Vega', NULL, '97889900', 'Ingeniería Materiales', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM estudiantes WHERE dni = '77889900' OR codigo_estudiante = 'EST-77889900');
    SET @estudiante_12 = (SELECT MIN(id_estudiante) FROM estudiantes WHERE dni = '77889900' OR codigo_estudiante = 'EST-77889900');
    INSERT INTO estudiante_area_historial (id_estudiante, id_area, fecha_inicio)
    SELECT @estudiante_12, @area_1, '2026-11-01' WHERE NOT EXISTS (SELECT 1 FROM estudiante_area_historial WHERE id_estudiante = @estudiante_12 AND fecha_fin IS NULL);
    INSERT INTO estudiantes (codigo_estudiante, dni, nombres, apellidos, fecha_nacimiento, telefono, carrera_interes, estado)
    SELECT 'EST-77325901', '77325901', 'Jose', 'Flores', NULL, '97325901', 'Enfermería', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM estudiantes WHERE dni = '77325901' OR codigo_estudiante = 'EST-77325901');
    SET @estudiante_13 = (SELECT MIN(id_estudiante) FROM estudiantes WHERE dni = '77325901' OR codigo_estudiante = 'EST-77325901');
    INSERT INTO estudiante_area_historial (id_estudiante, id_area, fecha_inicio)
    SELECT @estudiante_13, @area_2, '2026-11-01' WHERE NOT EXISTS (SELECT 1 FROM estudiante_area_historial WHERE id_estudiante = @estudiante_13 AND fecha_fin IS NULL);
    INSERT INTO estudiantes (codigo_estudiante, dni, nombres, apellidos, fecha_nacimiento, telefono, carrera_interes, estado)
    SELECT 'EST-73290801', '73290801', 'Roberto', 'Castro Mendoza', NULL, '93290801', 'Biología', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM estudiantes WHERE dni = '73290801' OR codigo_estudiante = 'EST-73290801');
    SET @estudiante_14 = (SELECT MIN(id_estudiante) FROM estudiantes WHERE dni = '73290801' OR codigo_estudiante = 'EST-73290801');
    INSERT INTO estudiante_area_historial (id_estudiante, id_area, fecha_inicio)
    SELECT @estudiante_14, @area_2, '2026-11-01' WHERE NOT EXISTS (SELECT 1 FROM estudiante_area_historial WHERE id_estudiante = @estudiante_14 AND fecha_fin IS NULL);
    INSERT INTO estudiantes (codigo_estudiante, dni, nombres, apellidos, fecha_nacimiento, telefono, carrera_interes, estado)
    SELECT 'EST-79934075', '79934075', 'Patricia', 'Ortiz Torres', NULL, '99934075', 'Agronomía', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM estudiantes WHERE dni = '79934075' OR codigo_estudiante = 'EST-79934075');
    SET @estudiante_15 = (SELECT MIN(id_estudiante) FROM estudiantes WHERE dni = '79934075' OR codigo_estudiante = 'EST-79934075');
    INSERT INTO estudiante_area_historial (id_estudiante, id_area, fecha_inicio)
    SELECT @estudiante_15, @area_2, '2026-11-01' WHERE NOT EXISTS (SELECT 1 FROM estudiante_area_historial WHERE id_estudiante = @estudiante_15 AND fecha_fin IS NULL);
    INSERT INTO estudiantes (codigo_estudiante, dni, nombres, apellidos, fecha_nacimiento, telefono, carrera_interes, estado)
    SELECT 'EST-74301232', '74301232', 'Fernando', 'Jiménez Vargas', NULL, '94301232', 'Ciencias de la Nutrición', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM estudiantes WHERE dni = '74301232' OR codigo_estudiante = 'EST-74301232');
    SET @estudiante_16 = (SELECT MIN(id_estudiante) FROM estudiantes WHERE dni = '74301232' OR codigo_estudiante = 'EST-74301232');
    INSERT INTO estudiante_area_historial (id_estudiante, id_area, fecha_inicio)
    SELECT @estudiante_16, @area_2, '2026-11-01' WHERE NOT EXISTS (SELECT 1 FROM estudiante_area_historial WHERE id_estudiante = @estudiante_16 AND fecha_fin IS NULL);
    INSERT INTO estudiantes (codigo_estudiante, dni, nombres, apellidos, fecha_nacimiento, telefono, carrera_interes, estado)
    SELECT 'EST-74049844', '74049844', 'Lucía', 'Moreno Ríos', NULL, '94049844', 'Ingeniería Pesquera', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM estudiantes WHERE dni = '74049844' OR codigo_estudiante = 'EST-74049844');
    SET @estudiante_17 = (SELECT MIN(id_estudiante) FROM estudiantes WHERE dni = '74049844' OR codigo_estudiante = 'EST-74049844');
    INSERT INTO estudiante_area_historial (id_estudiante, id_area, fecha_inicio)
    SELECT @estudiante_17, @area_2, '2026-11-01' WHERE NOT EXISTS (SELECT 1 FROM estudiante_area_historial WHERE id_estudiante = @estudiante_17 AND fecha_fin IS NULL);
    INSERT INTO estudiantes (codigo_estudiante, dni, nombres, apellidos, fecha_nacimiento, telefono, carrera_interes, estado)
    SELECT 'EST-75830680', '75830680', 'Sofía', 'González Castro', NULL, '95830680', 'Medicina', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM estudiantes WHERE dni = '75830680' OR codigo_estudiante = 'EST-75830680');
    SET @estudiante_18 = (SELECT MIN(id_estudiante) FROM estudiantes WHERE dni = '75830680' OR codigo_estudiante = 'EST-75830680');
    INSERT INTO estudiante_area_historial (id_estudiante, id_area, fecha_inicio)
    SELECT @estudiante_18, @area_2, '2026-11-01' WHERE NOT EXISTS (SELECT 1 FROM estudiante_area_historial WHERE id_estudiante = @estudiante_18 AND fecha_fin IS NULL);
    INSERT INTO estudiantes (codigo_estudiante, dni, nombres, apellidos, fecha_nacimiento, telefono, carrera_interes, estado)
    SELECT 'EST-74998424', '74998424', 'Diego', 'Ramírez Herrera', NULL, '94998424', 'Enfermería', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM estudiantes WHERE dni = '74998424' OR codigo_estudiante = 'EST-74998424');
    SET @estudiante_19 = (SELECT MIN(id_estudiante) FROM estudiantes WHERE dni = '74998424' OR codigo_estudiante = 'EST-74998424');
    INSERT INTO estudiante_area_historial (id_estudiante, id_area, fecha_inicio)
    SELECT @estudiante_19, @area_2, '2026-11-01' WHERE NOT EXISTS (SELECT 1 FROM estudiante_area_historial WHERE id_estudiante = @estudiante_19 AND fecha_fin IS NULL);
    INSERT INTO estudiantes (codigo_estudiante, dni, nombres, apellidos, fecha_nacimiento, telefono, carrera_interes, estado)
    SELECT 'EST-78912345', '78912345', 'Alejandra', 'Vega Soto', NULL, '98912345', 'Medicina', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM estudiantes WHERE dni = '78912345' OR codigo_estudiante = 'EST-78912345');
    SET @estudiante_20 = (SELECT MIN(id_estudiante) FROM estudiantes WHERE dni = '78912345' OR codigo_estudiante = 'EST-78912345');
    INSERT INTO estudiante_area_historial (id_estudiante, id_area, fecha_inicio)
    SELECT @estudiante_20, @area_2, '2026-11-01' WHERE NOT EXISTS (SELECT 1 FROM estudiante_area_historial WHERE id_estudiante = @estudiante_20 AND fecha_fin IS NULL);
    INSERT INTO estudiantes (codigo_estudiante, dni, nombres, apellidos, fecha_nacimiento, telefono, carrera_interes, estado)
    SELECT 'EST-75678901', '75678901', 'Ricardo', 'Morales Díaz', NULL, '95678901', 'Enfermería', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM estudiantes WHERE dni = '75678901' OR codigo_estudiante = 'EST-75678901');
    SET @estudiante_21 = (SELECT MIN(id_estudiante) FROM estudiantes WHERE dni = '75678901' OR codigo_estudiante = 'EST-75678901');
    INSERT INTO estudiante_area_historial (id_estudiante, id_area, fecha_inicio)
    SELECT @estudiante_21, @area_2, '2026-11-01' WHERE NOT EXISTS (SELECT 1 FROM estudiante_area_historial WHERE id_estudiante = @estudiante_21 AND fecha_fin IS NULL);
    INSERT INTO estudiantes (codigo_estudiante, dni, nombres, apellidos, fecha_nacimiento, telefono, carrera_interes, estado)
    SELECT 'EST-72345678', '72345678', 'Verónica', 'Cordero Luna', NULL, '92345678', 'Medicina', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM estudiantes WHERE dni = '72345678' OR codigo_estudiante = 'EST-72345678');
    SET @estudiante_22 = (SELECT MIN(id_estudiante) FROM estudiantes WHERE dni = '72345678' OR codigo_estudiante = 'EST-72345678');
    INSERT INTO estudiante_area_historial (id_estudiante, id_area, fecha_inicio)
    SELECT @estudiante_22, @area_2, '2026-11-01' WHERE NOT EXISTS (SELECT 1 FROM estudiante_area_historial WHERE id_estudiante = @estudiante_22 AND fecha_fin IS NULL);
    INSERT INTO estudiantes (codigo_estudiante, dni, nombres, apellidos, fecha_nacimiento, telefono, carrera_interes, estado)
    SELECT 'EST-75932855', '75932855', 'Valeria', 'Torres Mendoza', NULL, '95932855', 'Psicología', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM estudiantes WHERE dni = '75932855' OR codigo_estudiante = 'EST-75932855');
    SET @estudiante_23 = (SELECT MIN(id_estudiante) FROM estudiantes WHERE dni = '75932855' OR codigo_estudiante = 'EST-75932855');
    INSERT INTO estudiante_area_historial (id_estudiante, id_area, fecha_inicio)
    SELECT @estudiante_23, @area_3, '2026-11-01' WHERE NOT EXISTS (SELECT 1 FROM estudiante_area_historial WHERE id_estudiante = @estudiante_23 AND fecha_fin IS NULL);
    INSERT INTO estudiantes (codigo_estudiante, dni, nombres, apellidos, fecha_nacimiento, telefono, carrera_interes, estado)
    SELECT 'EST-78690126', '78690126', 'Andrés', 'Vargas Silva', NULL, '98690126', 'Derecho', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM estudiantes WHERE dni = '78690126' OR codigo_estudiante = 'EST-78690126');
    SET @estudiante_24 = (SELECT MIN(id_estudiante) FROM estudiantes WHERE dni = '78690126' OR codigo_estudiante = 'EST-78690126');
    INSERT INTO estudiante_area_historial (id_estudiante, id_area, fecha_inicio)
    SELECT @estudiante_24, @area_3, '2026-11-01' WHERE NOT EXISTS (SELECT 1 FROM estudiante_area_historial WHERE id_estudiante = @estudiante_24 AND fecha_fin IS NULL);
    INSERT INTO estudiantes (codigo_estudiante, dni, nombres, apellidos, fecha_nacimiento, telefono, carrera_interes, estado)
    SELECT 'EST-79567807', '79567807', 'Camila', 'Reyes López', NULL, '99567807', 'Administración', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM estudiantes WHERE dni = '79567807' OR codigo_estudiante = 'EST-79567807');
    SET @estudiante_25 = (SELECT MIN(id_estudiante) FROM estudiantes WHERE dni = '79567807' OR codigo_estudiante = 'EST-79567807');
    INSERT INTO estudiante_area_historial (id_estudiante, id_area, fecha_inicio)
    SELECT @estudiante_25, @area_3, '2026-11-01' WHERE NOT EXISTS (SELECT 1 FROM estudiante_area_historial WHERE id_estudiante = @estudiante_25 AND fecha_fin IS NULL);
    INSERT INTO estudiantes (codigo_estudiante, dni, nombres, apellidos, fecha_nacimiento, telefono, carrera_interes, estado)
    SELECT 'EST-76690451', '76690451', 'Miguel', 'Soto Pérez', NULL, '96690451', 'Contabilidad', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM estudiantes WHERE dni = '76690451' OR codigo_estudiante = 'EST-76690451');
    SET @estudiante_26 = (SELECT MIN(id_estudiante) FROM estudiantes WHERE dni = '76690451' OR codigo_estudiante = 'EST-76690451');
    INSERT INTO estudiante_area_historial (id_estudiante, id_area, fecha_inicio)
    SELECT @estudiante_26, @area_3, '2026-11-01' WHERE NOT EXISTS (SELECT 1 FROM estudiante_area_historial WHERE id_estudiante = @estudiante_26 AND fecha_fin IS NULL);
    INSERT INTO estudiantes (codigo_estudiante, dni, nombres, apellidos, fecha_nacimiento, telefono, carrera_interes, estado)
    SELECT 'EST-79597455', '79597455', 'Daniela', 'Cruz Vega', NULL, '99597455', 'Ciencias de la Comunicación', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM estudiantes WHERE dni = '79597455' OR codigo_estudiante = 'EST-79597455');
    SET @estudiante_27 = (SELECT MIN(id_estudiante) FROM estudiantes WHERE dni = '79597455' OR codigo_estudiante = 'EST-79597455');
    INSERT INTO estudiante_area_historial (id_estudiante, id_area, fecha_inicio)
    SELECT @estudiante_27, @area_3, '2026-11-01' WHERE NOT EXISTS (SELECT 1 FROM estudiante_area_historial WHERE id_estudiante = @estudiante_27 AND fecha_fin IS NULL);
    INSERT INTO estudiantes (codigo_estudiante, dni, nombres, apellidos, fecha_nacimiento, telefono, carrera_interes, estado)
    SELECT 'EST-75069262', '75069262', 'Alejandro', 'Mendoza Ruiz', NULL, '95069262', 'Economía', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM estudiantes WHERE dni = '75069262' OR codigo_estudiante = 'EST-75069262');
    SET @estudiante_28 = (SELECT MIN(id_estudiante) FROM estudiantes WHERE dni = '75069262' OR codigo_estudiante = 'EST-75069262');
    INSERT INTO estudiante_area_historial (id_estudiante, id_area, fecha_inicio)
    SELECT @estudiante_28, @area_3, '2026-11-01' WHERE NOT EXISTS (SELECT 1 FROM estudiante_area_historial WHERE id_estudiante = @estudiante_28 AND fecha_fin IS NULL);
    INSERT INTO estudiantes (codigo_estudiante, dni, nombres, apellidos, fecha_nacimiento, telefono, carrera_interes, estado)
    SELECT 'EST-79237042', '79237042', 'Isabella', 'Herrera Morales', NULL, '99237042', 'Turismo y Hotelería', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM estudiantes WHERE dni = '79237042' OR codigo_estudiante = 'EST-79237042');
    SET @estudiante_29 = (SELECT MIN(id_estudiante) FROM estudiantes WHERE dni = '79237042' OR codigo_estudiante = 'EST-79237042');
    INSERT INTO estudiante_area_historial (id_estudiante, id_area, fecha_inicio)
    SELECT @estudiante_29, @area_3, '2026-11-01' WHERE NOT EXISTS (SELECT 1 FROM estudiante_area_historial WHERE id_estudiante = @estudiante_29 AND fecha_fin IS NULL);
    INSERT INTO estudiantes (codigo_estudiante, dni, nombres, apellidos, fecha_nacimiento, telefono, carrera_interes, estado)
    SELECT 'EST-71638852', '71638852', 'Sebastián', 'López Torres', NULL, '91638852', 'Marketing', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM estudiantes WHERE dni = '71638852' OR codigo_estudiante = 'EST-71638852');
    SET @estudiante_30 = (SELECT MIN(id_estudiante) FROM estudiantes WHERE dni = '71638852' OR codigo_estudiante = 'EST-71638852');
    INSERT INTO estudiante_area_historial (id_estudiante, id_area, fecha_inicio)
    SELECT @estudiante_30, @area_3, '2026-11-01' WHERE NOT EXISTS (SELECT 1 FROM estudiante_area_historial WHERE id_estudiante = @estudiante_30 AND fecha_fin IS NULL);
    INSERT INTO estudiantes (codigo_estudiante, dni, nombres, apellidos, fecha_nacimiento, telefono, carrera_interes, estado)
    SELECT 'EST-74567890', '74567890', 'Mariana', 'Fuentes Ríos', NULL, '94567890', 'Trabajo Social', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM estudiantes WHERE dni = '74567890' OR codigo_estudiante = 'EST-74567890');
    SET @estudiante_31 = (SELECT MIN(id_estudiante) FROM estudiantes WHERE dni = '74567890' OR codigo_estudiante = 'EST-74567890');
    INSERT INTO estudiante_area_historial (id_estudiante, id_area, fecha_inicio)
    SELECT @estudiante_31, @area_3, '2026-11-01' WHERE NOT EXISTS (SELECT 1 FROM estudiante_area_historial WHERE id_estudiante = @estudiante_31 AND fecha_fin IS NULL);
    INSERT INTO estudiantes (codigo_estudiante, dni, nombres, apellidos, fecha_nacimiento, telefono, carrera_interes, estado)
    SELECT 'EST-71234569', '71234569', 'Felipe', 'Acosta Méndez', NULL, '91234569', 'Sociología', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM estudiantes WHERE dni = '71234569' OR codigo_estudiante = 'EST-71234569');
    SET @estudiante_32 = (SELECT MIN(id_estudiante) FROM estudiantes WHERE dni = '71234569' OR codigo_estudiante = 'EST-71234569');
    INSERT INTO estudiante_area_historial (id_estudiante, id_area, fecha_inicio)
    SELECT @estudiante_32, @area_3, '2026-11-01' WHERE NOT EXISTS (SELECT 1 FROM estudiante_area_historial WHERE id_estudiante = @estudiante_32 AND fecha_fin IS NULL);

    -- Aplicación de admisión y distribución de preguntas por área.
    SET @coordinador = (SELECT MIN(id_usuario) FROM usuarios WHERE username = 'coordinador' AND estado = 'ACTIVO');
    IF @coordinador IS NULL THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Se requiere la cuenta coordinador activa'; END IF;
    INSERT INTO ciclos_preparacion (nombre, fecha_inicio, fecha_fin, estado)
    SELECT 'Admisión 2026', '2026-01-01', '2026-12-31', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM ciclos_preparacion WHERE nombre = 'Admisión 2026');
    SET @ciclo = (SELECT MIN(id_ciclo) FROM ciclos_preparacion WHERE nombre = 'Admisión 2026');
    INSERT INTO simulacros (id_ciclo, nombre, fecha, estado, creado_por)
    SELECT @ciclo, 'Admisión 2026', '2026-11-01', 'ABIERTO', @coordinador WHERE NOT EXISTS (SELECT 1 FROM simulacros WHERE id_ciclo = @ciclo AND nombre = 'Admisión 2026' AND fecha = '2026-11-01');
    SET @simulacro = (SELECT MIN(id_simulacro) FROM simulacros WHERE id_ciclo = @ciclo AND nombre = 'Admisión 2026' AND fecha = '2026-11-01');
    INSERT INTO examenes (id_simulacro, id_area, nombre, descripcion, fecha_programada, estado, puntaje_total, creado_por, admite_preguntas)
    SELECT @simulacro, @area_1, 'Admisión 2026 - Ingenierías', 'Distribución de 80 preguntas por materias.', '2026-11-01', 'CONFIGURACION', 100.000000000, @coordinador, 1 WHERE NOT EXISTS (SELECT 1 FROM examenes WHERE id_simulacro = @simulacro AND id_area = @area_1);
    SET @examen_1 = (SELECT MIN(id_examen) FROM examenes WHERE id_simulacro = @simulacro AND id_area = @area_1);
    INSERT INTO examen_ejes (id_examen, id_eje, peso_porcentaje)
    SELECT @examen_1, @eje_1, 24.999999800 WHERE NOT EXISTS (SELECT 1 FROM examen_ejes WHERE id_examen = @examen_1 AND id_eje = @eje_1);
    INSERT INTO examen_ejes (id_examen, id_eje, peso_porcentaje)
    SELECT @examen_1, @eje_2, 7.000000000 WHERE NOT EXISTS (SELECT 1 FROM examen_ejes WHERE id_examen = @examen_1 AND id_eje = @eje_2);
    INSERT INTO examen_ejes (id_examen, id_eje, peso_porcentaje)
    SELECT @examen_1, @eje_5, 20.000000000 WHERE NOT EXISTS (SELECT 1 FROM examen_ejes WHERE id_examen = @examen_1 AND id_eje = @eje_5);
    INSERT INTO examen_ejes (id_examen, id_eje, peso_porcentaje)
    SELECT @examen_1, @eje_6, 10.000000000 WHERE NOT EXISTS (SELECT 1 FROM examen_ejes WHERE id_examen = @examen_1 AND id_eje = @eje_6);
    INSERT INTO examen_ejes (id_examen, id_eje, peso_porcentaje)
    SELECT @examen_1, @eje_7, 24.999999500 WHERE NOT EXISTS (SELECT 1 FROM examen_ejes WHERE id_examen = @examen_1 AND id_eje = @eje_7);
    INSERT INTO examen_ejes (id_examen, id_eje, peso_porcentaje)
    SELECT @examen_1, @eje_8, 8.000000000 WHERE NOT EXISTS (SELECT 1 FROM examen_ejes WHERE id_examen = @examen_1 AND id_eje = @eje_8);
    INSERT INTO examen_ejes (id_examen, id_eje, peso_porcentaje)
    SELECT @examen_1, @eje_9, 5.000000000 WHERE NOT EXISTS (SELECT 1 FROM examen_ejes WHERE id_examen = @examen_1 AND id_eje = @eje_9);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_1, @materia_2, 1, 4, 1.124150000 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_1 AND id_materia = @materia_2);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_1, @materia_3, 2, 5, 1.100680000 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_1 AND id_materia = @materia_3);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_1, @materia_4, 3, 4, 1.124150000 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_1 AND id_materia = @materia_4);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_1, @materia_5, 4, 5, 1.100680000 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_1 AND id_materia = @materia_5);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_1, @materia_6, 5, 4, 1.658337400 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_1 AND id_materia = @materia_6);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_1, @materia_7, 6, 4, 1.658267400 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_1 AND id_materia = @materia_7);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_1, @materia_8, 7, 4, 1.658787400 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_1 AND id_materia = @materia_8);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_1, @materia_9, 8, 3, 1.699477000 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_1 AND id_materia = @materia_9);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_1, @materia_10, 9, 4, 1.289859000 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_1 AND id_materia = @materia_10);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_1, @materia_11, 10, 4, 1.210141000 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_1 AND id_materia = @materia_11);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_1, @materia_12, 11, 6, 1.425411400 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_1 AND id_materia = @materia_12);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_1, @materia_13, 12, 5, 1.154748700 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_1 AND id_materia = @materia_13);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_1, @materia_14, 13, 7, 1.524826800 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_1 AND id_materia = @materia_14);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_1, @materia_15, 14, 3, 0.798740000 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_1 AND id_materia = @materia_15);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_1, @materia_16, 15, 4, 0.801890000 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_1 AND id_materia = @materia_16);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_1, @materia_17, 16, 3, 0.798740000 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_1 AND id_materia = @materia_17);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_1, @materia_18, 17, 4, 1.021414000 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_1 AND id_materia = @materia_18);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_1, @materia_19, 18, 3, 0.971448000 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_1 AND id_materia = @materia_19);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_1, @materia_20, 19, 2, 1.258700000 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_1 AND id_materia = @materia_20);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_1, @materia_21, 20, 2, 1.241300000 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_1 AND id_materia = @materia_21);
    INSERT INTO examenes (id_simulacro, id_area, nombre, descripcion, fecha_programada, estado, puntaje_total, creado_por, admite_preguntas)
    SELECT @simulacro, @area_2, 'Admisión 2026 - Biomédicas', 'Distribución de 80 preguntas por materias.', '2026-11-01', 'CONFIGURACION', 100.000000000, @coordinador, 1 WHERE NOT EXISTS (SELECT 1 FROM examenes WHERE id_simulacro = @simulacro AND id_area = @area_2);
    SET @examen_2 = (SELECT MIN(id_examen) FROM examenes WHERE id_simulacro = @simulacro AND id_area = @area_2);
    INSERT INTO examen_ejes (id_examen, id_eje, peso_porcentaje)
    SELECT @examen_2, @eje_1, 15.000000000 WHERE NOT EXISTS (SELECT 1 FROM examen_ejes WHERE id_examen = @examen_2 AND id_eje = @eje_1);
    INSERT INTO examen_ejes (id_examen, id_eje, peso_porcentaje)
    SELECT @examen_2, @eje_2, 7.000000000 WHERE NOT EXISTS (SELECT 1 FROM examen_ejes WHERE id_examen = @examen_2 AND id_eje = @eje_2);
    INSERT INTO examen_ejes (id_examen, id_eje, peso_porcentaje)
    SELECT @examen_2, @eje_5, 20.000000000 WHERE NOT EXISTS (SELECT 1 FROM examen_ejes WHERE id_examen = @examen_2 AND id_eje = @eje_5);
    INSERT INTO examen_ejes (id_examen, id_eje, peso_porcentaje)
    SELECT @examen_2, @eje_6, 10.000000000 WHERE NOT EXISTS (SELECT 1 FROM examen_ejes WHERE id_examen = @examen_2 AND id_eje = @eje_6);
    INSERT INTO examen_ejes (id_examen, id_eje, peso_porcentaje)
    SELECT @examen_2, @eje_7, 35.000000000 WHERE NOT EXISTS (SELECT 1 FROM examen_ejes WHERE id_examen = @examen_2 AND id_eje = @eje_7);
    INSERT INTO examen_ejes (id_examen, id_eje, peso_porcentaje)
    SELECT @examen_2, @eje_8, 8.000000000 WHERE NOT EXISTS (SELECT 1 FROM examen_ejes WHERE id_examen = @examen_2 AND id_eje = @eje_8);
    INSERT INTO examen_ejes (id_examen, id_eje, peso_porcentaje)
    SELECT @examen_2, @eje_9, 5.000000000 WHERE NOT EXISTS (SELECT 1 FROM examen_ejes WHERE id_examen = @examen_2 AND id_eje = @eje_9);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_2, @materia_2, 1, 4, 1.124150000 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_2 AND id_materia = @materia_2);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_2, @materia_3, 2, 5, 1.100680000 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_2 AND id_materia = @materia_3);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_2, @materia_4, 3, 4, 1.124150000 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_2 AND id_materia = @materia_4);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_2, @materia_5, 4, 5, 1.100680000 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_2 AND id_materia = @materia_5);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_2, @materia_6, 5, 3, 1.265447400 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_2 AND id_materia = @materia_6);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_2, @materia_7, 6, 3, 1.265447400 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_2 AND id_materia = @materia_7);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_2, @materia_8, 7, 3, 1.265447400 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_2 AND id_materia = @materia_8);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_2, @materia_9, 8, 3, 1.203657800 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_2 AND id_materia = @materia_9);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_2, @materia_10, 9, 5, 1.123540000 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_2 AND id_materia = @materia_10);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_2, @materia_11, 10, 4, 1.095575000 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_2 AND id_materia = @materia_11);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_2, @materia_12, 11, 6, 1.684740000 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_2 AND id_materia = @materia_12);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_2, @materia_13, 12, 9, 1.945140000 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_2 AND id_materia = @materia_13);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_2, @materia_14, 13, 5, 1.477060000 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_2 AND id_materia = @materia_14);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_2, @materia_15, 14, 3, 0.798740000 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_2 AND id_materia = @materia_15);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_2, @materia_16, 15, 4, 0.801890000 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_2 AND id_materia = @materia_16);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_2, @materia_17, 16, 3, 0.798740000 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_2 AND id_materia = @materia_17);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_2, @materia_18, 17, 4, 1.021414000 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_2 AND id_materia = @materia_18);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_2, @materia_19, 18, 3, 0.971448000 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_2 AND id_materia = @materia_19);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_2, @materia_20, 19, 2, 1.258700000 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_2 AND id_materia = @materia_20);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_2, @materia_21, 20, 2, 1.241300000 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_2 AND id_materia = @materia_21);
    INSERT INTO examenes (id_simulacro, id_area, nombre, descripcion, fecha_programada, estado, puntaje_total, creado_por, admite_preguntas)
    SELECT @simulacro, @area_3, 'Admisión 2026 - Sociales', 'Distribución de 80 preguntas por materias.', '2026-11-01', 'CONFIGURACION', 100.000000000, @coordinador, 1 WHERE NOT EXISTS (SELECT 1 FROM examenes WHERE id_simulacro = @simulacro AND id_area = @area_3);
    SET @examen_3 = (SELECT MIN(id_examen) FROM examenes WHERE id_simulacro = @simulacro AND id_area = @area_3);
    INSERT INTO examen_ejes (id_examen, id_eje, peso_porcentaje)
    SELECT @examen_3, @eje_1, 9.999999900 WHERE NOT EXISTS (SELECT 1 FROM examen_ejes WHERE id_examen = @examen_3 AND id_eje = @eje_1);
    INSERT INTO examen_ejes (id_examen, id_eje, peso_porcentaje)
    SELECT @examen_3, @eje_2, 22.000000000 WHERE NOT EXISTS (SELECT 1 FROM examen_ejes WHERE id_examen = @examen_3 AND id_eje = @eje_2);
    INSERT INTO examen_ejes (id_examen, id_eje, peso_porcentaje)
    SELECT @examen_3, @eje_5, 20.000000000 WHERE NOT EXISTS (SELECT 1 FROM examen_ejes WHERE id_examen = @examen_3 AND id_eje = @eje_5);
    INSERT INTO examen_ejes (id_examen, id_eje, peso_porcentaje)
    SELECT @examen_3, @eje_6, 23.000000000 WHERE NOT EXISTS (SELECT 1 FROM examen_ejes WHERE id_examen = @examen_3 AND id_eje = @eje_6);
    INSERT INTO examen_ejes (id_examen, id_eje, peso_porcentaje)
    SELECT @examen_3, @eje_7, 9.999999300 WHERE NOT EXISTS (SELECT 1 FROM examen_ejes WHERE id_examen = @examen_3 AND id_eje = @eje_7);
    INSERT INTO examen_ejes (id_examen, id_eje, peso_porcentaje)
    SELECT @examen_3, @eje_8, 10.000000000 WHERE NOT EXISTS (SELECT 1 FROM examen_ejes WHERE id_examen = @examen_3 AND id_eje = @eje_8);
    INSERT INTO examen_ejes (id_examen, id_eje, peso_porcentaje)
    SELECT @examen_3, @eje_9, 5.000000000 WHERE NOT EXISTS (SELECT 1 FROM examen_ejes WHERE id_examen = @examen_3 AND id_eje = @eje_9);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_3, @materia_2, 1, 4, 1.124150000 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_3 AND id_materia = @materia_2);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_3, @materia_3, 2, 5, 1.100680000 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_3 AND id_materia = @materia_3);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_3, @materia_4, 3, 4, 1.124150000 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_3 AND id_materia = @materia_4);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_3, @materia_5, 4, 5, 1.100680000 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_3 AND id_materia = @materia_5);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_3, @materia_6, 5, 3, 0.824574000 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_3 AND id_materia = @materia_6);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_3, @materia_7, 6, 3, 0.824134300 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_3 AND id_materia = @materia_7);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_3, @materia_8, 7, 3, 0.825011500 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_3 AND id_materia = @materia_8);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_3, @materia_9, 8, 3, 0.859613500 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_3 AND id_materia = @materia_9);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_3, @materia_10, 9, 8, 1.774740000 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_3 AND id_materia = @materia_10);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_3, @materia_11, 10, 5, 1.760416000 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_3 AND id_materia = @materia_11);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_3, @materia_12, 11, 3, 1.109300700 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_3 AND id_materia = @materia_12);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_3, @materia_13, 12, 3, 1.146903300 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_3 AND id_materia = @materia_13);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_3, @materia_14, 13, 3, 1.077129100 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_3 AND id_materia = @materia_14);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_3, @materia_15, 14, 3, 0.887877000 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_3 AND id_materia = @materia_15);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_3, @materia_16, 15, 5, 0.934547600 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_3 AND id_materia = @materia_16);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_3, @materia_17, 16, 3, 0.887877000 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_3 AND id_materia = @materia_17);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_3, @materia_18, 17, 8, 1.701541000 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_3 AND id_materia = @materia_18);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_3, @materia_19, 18, 5, 1.677534400 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_3 AND id_materia = @materia_19);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_3, @materia_20, 19, 2, 1.258700000 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_3 AND id_materia = @materia_20);
    INSERT INTO distribucion_examen (id_examen, id_materia, orden, cantidad_preguntas, puntaje_por_pregunta)
    SELECT @examen_3, @materia_21, 20, 2, 1.241300000 WHERE NOT EXISTS (SELECT 1 FROM distribucion_examen WHERE id_examen = @examen_3 AND id_materia = @materia_21);
    COMMIT;
END$$
CALL sp_cargar_datos_iniciales_academicos()$$
DROP PROCEDURE sp_cargar_datos_iniciales_academicos$$
DELIMITER ;

-- Resumen de las configuraciones insertadas.
SELECT a.nombre AS area, SUM(d.cantidad_preguntas) AS cantidad_preguntas,
       SUM(d.puntaje_asignado) AS puntaje_total
FROM examenes e JOIN areas a ON a.id_area = e.id_area
JOIN distribucion_examen d ON d.id_examen = e.id_examen
WHERE e.id_examen IN (@examen_1, @examen_2, @examen_3)
GROUP BY e.id_examen, a.nombre ORDER BY a.nombre;

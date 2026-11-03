-- Diseño corregido 2026-10-03. Instalación NUEVA; no es una migración.
-- Contratos de aplicación y decisiones: 7_correcciones_y_criterios.md.
-- SOLO DESARROLLO: descomentar la siguiente línea para reiniciar la base (borra todos los datos).
-- DROP DATABASE IF EXISTS sistema_evaluacion;

CREATE DATABASE IF NOT EXISTS sistema_evaluacion
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE sistema_evaluacion;

CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    email VARCHAR(150),
    telefono VARCHAR(20),
    estado ENUM(
        'ACTIVO',
        'INACTIVO'
    ) DEFAULT 'ACTIVO',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE roles (
    id_rol INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion VARCHAR(255)
) ENGINE=InnoDB;

INSERT INTO roles(nombre,descripcion)
VALUES

('DIRECTOR',
'Administrador principal y acceso institucional'),

('COORDINADOR',
'Gestion académica y aprobación'),

('DOCENTE',
'Creación y gestión de preguntas'),

('ESTUDIANTE',
'Consulta resultados académicos');

CREATE TABLE usuario_roles (
    id_usuario INT,
    id_rol INT,
    PRIMARY KEY(
        id_usuario,
        id_rol
    ),
    FOREIGN KEY(id_usuario)
    REFERENCES usuarios(id_usuario),
    FOREIGN KEY(id_rol)
    REFERENCES roles(id_rol)
) ENGINE=InnoDB;

CREATE TABLE permisos (

    id_permiso INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(80) UNIQUE NOT NULL,
    descripcion VARCHAR(255)
) ENGINE=InnoDB;

INSERT INTO permisos(nombre,descripcion)
VALUES

('CREAR_PREGUNTA',
'Crear preguntas del banco'),

('EDITAR_PREGUNTA',
'Modificar preguntas'),

('APROBAR_PREGUNTA',
'Aprobar preguntas'),

('CREAR_EXAMEN',
'Crear examen'),

('CONFIGURAR_EXAMEN',
'Definir distribución'),

('PROCESAR_CARTILLA',
'Procesar resultados'),

('CORREGIR_CARTILLA',
'Corrección manual'),

('VER_RESULTADOS',
'Consulta resultados'),

('VER_PERFIL',
'Consulta perfil académico'),

('VER_RANKING',
'Consulta ranking'),

('GENERAR_REPORTES',
'Crear reportes');

CREATE TABLE rol_permisos (

    id_rol INT,
    id_permiso INT,
    PRIMARY KEY(
        id_rol,
        id_permiso
    ),
    FOREIGN KEY(id_rol)
    REFERENCES roles(id_rol),
    FOREIGN KEY(id_permiso)
    REFERENCES permisos(id_permiso)

) ENGINE=InnoDB;

CREATE TABLE paneles (

    id_panel INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    ruta VARCHAR(100)
) ENGINE=InnoDB;

INSERT INTO paneles(nombre,ruta)
VALUES

('Panel Director','/director'),

('Panel Coordinador','/coordinador'),

('Panel Docente','/docente'),

('Panel Estudiante','/estudiante');

CREATE TABLE rol_paneles (

    id_rol INT,

    id_panel INT,

    PRIMARY KEY(
        id_rol,
        id_panel
    ),

    FOREIGN KEY(id_rol)
    REFERENCES roles(id_rol),

    FOREIGN KEY(id_panel)
    REFERENCES paneles(id_panel)

) ENGINE=InnoDB;

USE sistema_evaluacion;

-- ============================================
-- BLOQUE 3
-- PERSONAS: ESTUDIANTES, DOCENTES,
-- COORDINADORES Y DIRECTORES
-- ============================================

-- ============================================
-- ESTUDIANTES
-- Un estudiante puede existir sin usuario
-- ============================================

CREATE TABLE estudiantes (

    id_estudiante INT AUTO_INCREMENT PRIMARY KEY,

    id_usuario INT NULL UNIQUE,

    codigo_estudiante VARCHAR(30) UNIQUE NOT NULL,

    dni VARCHAR(20),

    nombres VARCHAR(100) NOT NULL,

    apellidos VARCHAR(100) NOT NULL,

    fecha_nacimiento DATE,

    telefono VARCHAR(20),

    email VARCHAR(150),

    carrera_interes VARCHAR(150),

    estado ENUM(
        'ACTIVO',
        'INACTIVO'
    ) DEFAULT 'ACTIVO',

    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(id_usuario)
    REFERENCES usuarios(id_usuario)

) ENGINE=InnoDB;

-- ============================================
-- DOCENTES
-- ============================================

CREATE TABLE docentes (

    id_docente INT AUTO_INCREMENT PRIMARY KEY,

    id_usuario INT NOT NULL UNIQUE,

    codigo_docente VARCHAR(30) UNIQUE,

    especialidad VARCHAR(150),

    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(id_usuario)
    REFERENCES usuarios(id_usuario)

) ENGINE=InnoDB;

-- ============================================
-- COORDINADORES
-- ============================================

CREATE TABLE coordinadores (

    id_coordinador INT AUTO_INCREMENT PRIMARY KEY,

    id_usuario INT NOT NULL UNIQUE,

    cargo VARCHAR(100),

    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(id_usuario)
    REFERENCES usuarios(id_usuario)

) ENGINE=InnoDB;

-- ============================================
-- DIRECTORES
-- ============================================

CREATE TABLE directores (

    id_director INT AUTO_INCREMENT PRIMARY KEY,

    id_usuario INT NOT NULL UNIQUE,

    cargo VARCHAR(100),

    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(id_usuario)
    REFERENCES usuarios(id_usuario)

) ENGINE=InnoDB;

-- ============================================
-- AREAS ACADEMICAS
-- Ejemplo:
-- Ingenierías
-- Biomédicas
-- Sociales
-- ============================================

CREATE TABLE areas (

    id_area INT AUTO_INCREMENT PRIMARY KEY,

    codigo VARCHAR(50) UNIQUE NOT NULL,

    nombre VARCHAR(100) NOT NULL,

    descripcion TEXT,

    estado ENUM(
        'ACTIVO',
        'INACTIVO'
    ) DEFAULT 'ACTIVO',

    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP

) ENGINE=InnoDB;

-- ============================================
-- EJES TEMATICOS
-- Ejemplo:
-- Matemática
-- Comunicación
-- Ciencias
-- ============================================

CREATE TABLE ejes_tematicos (

    id_eje INT AUTO_INCREMENT PRIMARY KEY,

    nombre VARCHAR(100) NOT NULL,

    descripcion TEXT,

    estado ENUM(
        'ACTIVO',
        'INACTIVO'
    ) DEFAULT 'ACTIVO'

) ENGINE=InnoDB;

-- ============================================
-- MATERIAS
-- Pertenece a un eje temático; la misma materia se usa en todas las áreas
-- ============================================

CREATE TABLE materias (

    id_materia INT AUTO_INCREMENT PRIMARY KEY,

    id_eje INT NOT NULL,

    codigo VARCHAR(50) UNIQUE,

    nombre VARCHAR(100) NOT NULL,

    descripcion TEXT,

    valor_referencia DECIMAL(6,2),

    estado ENUM(
        'ACTIVO',
        'INACTIVO'
    ) DEFAULT 'ACTIVO',

    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(id_eje)
    REFERENCES ejes_tematicos(id_eje)

) ENGINE=InnoDB;

-- ============================================
-- RELACION DOCENTE - MATERIA
-- Un docente puede enseñar varias materias
-- ============================================

CREATE TABLE docente_materias (

    id_docente INT,

    id_materia INT,

    fecha_asignacion DATE,

    estado ENUM(
        'ACTIVO',
        'INACTIVO'
    ) DEFAULT 'ACTIVO',

    PRIMARY KEY(
        id_docente,
        id_materia
    ),

    FOREIGN KEY(id_docente)
    REFERENCES docentes(id_docente),

    FOREIGN KEY(id_materia)
    REFERENCES materias(id_materia)

) ENGINE=InnoDB;

-- ============================================
-- HISTORIAL DE AREA DEL ESTUDIANTE
-- Puede cambiar:
-- Ingeniería -> Sociales
-- ============================================

CREATE TABLE estudiante_area_historial (

    id_historial INT AUTO_INCREMENT PRIMARY KEY,

    id_estudiante INT NOT NULL,

    id_area INT NOT NULL,

    fecha_inicio DATE NOT NULL,

    fecha_fin DATE,

    activo BOOLEAN GENERATED ALWAYS AS (fecha_fin IS NULL) STORED,
    abierto_unico TINYINT GENERATED ALWAYS AS (IF(fecha_fin IS NULL, 1, NULL)) STORED,
    UNIQUE(id_estudiante, abierto_unico),
    UNIQUE(id_estudiante, fecha_inicio),
    CHECK (fecha_fin IS NULL OR fecha_fin > fecha_inicio),

    FOREIGN KEY(id_estudiante)
    REFERENCES estudiantes(id_estudiante),

    FOREIGN KEY(id_area)
    REFERENCES areas(id_area)

) ENGINE=InnoDB;

-- ============================================
-- CICLOS DE PREPARACION
-- Ejemplo:
-- PRE 2026-I
-- ============================================

CREATE TABLE ciclos_preparacion (

    id_ciclo INT AUTO_INCREMENT PRIMARY KEY,

    nombre VARCHAR(100) NOT NULL,

    fecha_inicio DATE,

    fecha_fin DATE,

    estado ENUM(
        'ACTIVO',
        'FINALIZADO',
        'INACTIVO'
    ) DEFAULT 'ACTIVO'

) ENGINE=InnoDB;

-- ============================================
-- GRUPOS ACADEMICOS
-- Ejemplo:
-- Grupo mañana
-- Grupo tarde
-- ============================================

CREATE TABLE grupos_academicos (

    id_grupo INT AUTO_INCREMENT PRIMARY KEY,

    id_ciclo INT NOT NULL,

    nombre VARCHAR(100),

    horario VARCHAR(100),

    aula VARCHAR(50),
    estado ENUM('ACTIVO','INACTIVO') NOT NULL DEFAULT 'ACTIVO',

    FOREIGN KEY(id_ciclo)
    REFERENCES ciclos_preparacion(id_ciclo)

) ENGINE=InnoDB;

-- ============================================
-- HISTORIAL GRUPO DEL ESTUDIANTE
-- ============================================

CREATE TABLE estudiante_grupo_historial (

    id_historial INT AUTO_INCREMENT PRIMARY KEY,

    id_estudiante INT NOT NULL,

    id_grupo INT NOT NULL,

    fecha_inicio DATE NOT NULL,

    fecha_fin DATE,

    activo BOOLEAN GENERATED ALWAYS AS (fecha_fin IS NULL) STORED,
    abierto_unico TINYINT GENERATED ALWAYS AS (IF(fecha_fin IS NULL, 1, NULL)) STORED,
    UNIQUE(id_estudiante, abierto_unico),
    UNIQUE(id_estudiante, fecha_inicio),
    CHECK (fecha_fin IS NULL OR fecha_fin > fecha_inicio),

    FOREIGN KEY(id_estudiante)
    REFERENCES estudiantes(id_estudiante),

    FOREIGN KEY(id_grupo)
    REFERENCES grupos_academicos(id_grupo)

) ENGINE=InnoDB;

USE sistema_evaluacion;

-- ============================================
-- BLOQUE 4
-- BANCO DE PREGUNTAS
-- ============================================

-- ============================================
-- PREGUNTAS
-- Estados:
-- BORRADOR
-- REVISION
-- APROBADA
-- INACTIVA
-- ============================================

CREATE TABLE preguntas (

    id_pregunta INT AUTO_INCREMENT PRIMARY KEY,

    id_examen_destino INT NULL,

    id_materia INT NOT NULL,

    id_autor_docente INT NOT NULL,

    estado ENUM(
        'BORRADOR',
        'REVISION',
        'APROBADA',
        'INACTIVA'
    ) DEFAULT 'BORRADOR',

    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    fecha_aprobacion DATETIME,

    aprobado_por INT NULL,

    FOREIGN KEY(id_materia)
    REFERENCES materias(id_materia),

    FOREIGN KEY(id_autor_docente)
    REFERENCES docentes(id_docente),

    FOREIGN KEY(aprobado_por)
    REFERENCES usuarios(id_usuario)

) ENGINE=InnoDB;

-- ============================================
-- VERSIONES DE PREGUNTAS
-- Para mantener historial
-- Una pregunta puede cambiar sin perder historial
-- ============================================

CREATE TABLE pregunta_versiones (

    id_version INT AUTO_INCREMENT PRIMARY KEY,

    id_pregunta INT NOT NULL,

    numero_version INT NOT NULL,
    sellada BOOLEAN NOT NULL DEFAULT FALSE,
    UNIQUE(id_version, id_pregunta),
    CHECK (numero_version > 0),

    enunciado TEXT NOT NULL,

    respuesta_correcta CHAR(1) NOT NULL,

    fecha_version TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    usuario_modifico INT,

    estado ENUM(
        'ACTIVA',
        'HISTORICA'
    ) DEFAULT 'ACTIVA',

    activa_unica TINYINT GENERATED ALWAYS AS (IF(estado = 'ACTIVA', 1, NULL)) STORED,
    UNIQUE(id_pregunta, numero_version),
    UNIQUE(id_pregunta, activa_unica),
    CHECK (respuesta_correcta IN ('A','B','C','D','E')),
    FOREIGN KEY(id_pregunta)
    REFERENCES preguntas(id_pregunta),

    FOREIGN KEY(usuario_modifico)
    REFERENCES usuarios(id_usuario)

) ENGINE=InnoDB;

-- ============================================
-- ALTERNATIVAS DE PREGUNTAS
-- A,B,C,D,E
-- ============================================

CREATE TABLE alternativas_pregunta (

    id_alternativa INT AUTO_INCREMENT PRIMARY KEY,
    id_version INT NOT NULL,
    letra CHAR(1) NOT NULL,
    contenido TEXT NULL,
    UNIQUE(id_version, letra),
    CHECK (letra IN ('A','B','C','D','E')),
    FOREIGN KEY(id_version)
    REFERENCES pregunta_versiones(id_version)
) ENGINE=InnoDB;

-- ============================================
-- TEMAS ESPECIFICOS
-- Ejemplo:
-- Matemática
-- Álgebra
-- Ecuaciones
-- ============================================

CREATE TABLE temas (

    id_tema INT AUTO_INCREMENT PRIMARY KEY,
    id_materia INT NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    FOREIGN KEY(id_materia)
    REFERENCES materias(id_materia)
) ENGINE=InnoDB;

-- ============================================
-- RELACION PREGUNTA - TEMA
-- Una pregunta pertenece a un tema
-- ============================================

CREATE TABLE pregunta_tema (
    id_pregunta INT PRIMARY KEY,
    id_tema INT NOT NULL,
    FOREIGN KEY(id_pregunta)
    REFERENCES preguntas(id_pregunta),
    FOREIGN KEY(id_tema)
    REFERENCES temas(id_tema)

) ENGINE=InnoDB;

-- ============================================
-- REVISION DE PREGUNTAS
-- El coordinador revisa
-- ============================================

CREATE TABLE revisiones_pregunta (
    id_revision INT AUTO_INCREMENT PRIMARY KEY,
    id_version_pregunta INT NOT NULL,
    id_pregunta INT NOT NULL,
    FOREIGN KEY(id_version_pregunta, id_pregunta) REFERENCES pregunta_versiones(id_version, id_pregunta),
    id_usuario_revision INT NOT NULL,
    estado_anterior VARCHAR(50),
    estado_nuevo VARCHAR(50),
    observacion TEXT,
    fecha_revision TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(id_pregunta)
    REFERENCES preguntas(id_pregunta),
    FOREIGN KEY(id_usuario_revision)
    REFERENCES usuarios(id_usuario)

) ENGINE=InnoDB;

USE sistema_evaluacion;

-- ============================================
-- BLOQUE 5
-- EXAMENES, VERSIONES Y CONFIGURACION
-- ============================================

-- ============================================
-- EXAMEN
-- Examen de admisión por área
-- Ejemplo:
-- Ingeniería Enero 2026
-- Biomédicas Febrero 2026
-- ============================================

CREATE TABLE simulacros (
    id_simulacro INT AUTO_INCREMENT PRIMARY KEY,
    id_ciclo INT NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    fecha DATE,
    estado ENUM(
        'ABIERTO',
        'CERRADO',
        'INACTIVO'
    ) DEFAULT 'ABIERTO',
    creado_por INT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(id_ciclo)
    REFERENCES ciclos_preparacion(id_ciclo),
    FOREIGN KEY(creado_por)
    REFERENCES usuarios(id_usuario)
) ENGINE=InnoDB;

CREATE TABLE examenes (

    id_examen INT AUTO_INCREMENT PRIMARY KEY,

    admite_preguntas BOOLEAN NOT NULL DEFAULT TRUE,

    id_simulacro INT NOT NULL,
    id_area INT NOT NULL,
    nombre VARCHAR(150) NOT NULL,

    descripcion TEXT,

    fecha_programada DATE,

    estado ENUM(
        'BORRADOR',
        'CONFIGURACION',
        'APROBADO',
        'APLICADO',
        'CERRADO'
    ) DEFAULT 'BORRADOR',

    puntaje_total DECIMAL(24,9) DEFAULT 100.00,

    creado_por INT NOT NULL,

    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(id_simulacro, id_area),
    UNIQUE(id_examen, id_simulacro),
    CHECK (puntaje_total > 0),
    FOREIGN KEY(id_simulacro)
    REFERENCES simulacros(id_simulacro),
    FOREIGN KEY(id_area)
    REFERENCES areas(id_area),
    FOREIGN KEY(creado_por)
    REFERENCES usuarios(id_usuario)

) ENGINE=InnoDB;

-- ============================================
-- VERSIONES DEL EXAMEN
-- Ejemplo:
-- Ingeniería Enero 2026
-- Version A
-- Version B
-- ============================================

CREATE TABLE versiones_examen (

    id_version INT AUTO_INCREMENT PRIMARY KEY,

    id_examen INT NOT NULL,

    codigo_version VARCHAR(20) NOT NULL,

    descripcion VARCHAR(150),

    estado ENUM(
        'ACTIVA',
        'INACTIVA'
    ) DEFAULT 'ACTIVA',

    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(id_examen, codigo_version),
    UNIQUE(id_version, id_examen),

    FOREIGN KEY(id_examen)
    REFERENCES examenes(id_examen)

) ENGINE=InnoDB;

-- ============================================
-- DISTRIBUCION DEL EXAMEN POR MATERIA
-- Define:
-- cantidad preguntas
-- peso
-- puntaje
-- ============================================

-- Pesos configurados por EJE, separados de la distribución por materia.
CREATE TABLE examen_ejes (
    id_examen INT NOT NULL,
    id_eje INT NOT NULL,
    peso_porcentaje DECIMAL(12,9) NOT NULL,
    PRIMARY KEY(id_examen, id_eje),
    CHECK (peso_porcentaje > 0 AND peso_porcentaje <= 100),
    FOREIGN KEY(id_examen) REFERENCES examenes(id_examen),
    FOREIGN KEY(id_eje) REFERENCES ejes_tematicos(id_eje)
) ENGINE=InnoDB;

CREATE TABLE distribucion_examen (

    id_distribucion INT AUTO_INCREMENT PRIMARY KEY,

    id_examen INT NOT NULL,

    id_materia INT NOT NULL,
    orden INT NOT NULL DEFAULT 1,
    cantidad_preguntas INT NOT NULL,


    puntaje_por_pregunta DECIMAL(24,9) NOT NULL,
    puntaje_asignado DECIMAL(24,9) GENERATED ALWAYS AS (cantidad_preguntas * puntaje_por_pregunta) STORED,
    CHECK (cantidad_preguntas > 0),
    CHECK (puntaje_por_pregunta > 0),

    UNIQUE(id_examen, id_materia),

    FOREIGN KEY(id_examen)
    REFERENCES examenes(id_examen),

    FOREIGN KEY(id_materia)
    REFERENCES materias(id_materia)

) ENGINE=InnoDB;

-- ============================================
-- PREGUNTAS QUE FORMAN PARTE DEL EXAMEN
-- Una pregunta puede reutilizarse
-- ============================================

CREATE TABLE examen_preguntas (

    id_examen_pregunta INT AUTO_INCREMENT PRIMARY KEY,

    id_version_examen INT NOT NULL,

    id_version_pregunta INT NOT NULL,

    numero_pregunta INT NOT NULL,

    puntaje DECIMAL(24,9) NOT NULL,
    CHECK (numero_pregunta > 0 AND puntaje > 0),
    UNIQUE(id_version_examen, id_version_pregunta),
    UNIQUE(id_examen_pregunta, id_version_examen, id_version_pregunta),
    UNIQUE(id_version_examen, numero_pregunta, id_version_pregunta),
    UNIQUE(id_version_examen, numero_pregunta),
    FOREIGN KEY(id_version_examen)
    REFERENCES versiones_examen(id_version),
    FOREIGN KEY(id_version_pregunta)
    REFERENCES pregunta_versiones(id_version)
) ENGINE=InnoDB;

-- ============================================
-- PLANTILLA DE RESPUESTAS POR VERSION
-- Usada por OpenCV
-- ============================================
-- Una revisión de clave no es una versión A/B del cuadernillo.
CREATE TABLE revisiones_clave (
    id_revision_clave INT AUTO_INCREMENT PRIMARY KEY,
    id_version_examen INT NOT NULL,
    numero_revision INT NOT NULL,
    estado ENUM('BORRADOR','CONFIRMADA') NOT NULL DEFAULT 'BORRADOR',
    creada_por INT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    motivo TEXT NOT NULL,
    UNIQUE(id_version_examen, numero_revision),
    UNIQUE(id_revision_clave, id_version_examen),
    CHECK (numero_revision > 0 AND CHAR_LENGTH(TRIM(motivo)) > 0),
    FOREIGN KEY(id_version_examen) REFERENCES versiones_examen(id_version),
    FOREIGN KEY(creada_por) REFERENCES usuarios(id_usuario)
) ENGINE=InnoDB;

CREATE TABLE plantilla_respuestas (

    id_plantilla INT AUTO_INCREMENT PRIMARY KEY,
    id_revision_clave INT NOT NULL,

    id_version_examen INT NOT NULL,

    numero_pregunta INT NOT NULL,

    id_version_pregunta INT NOT NULL,

    respuesta_correcta CHAR(1) NOT NULL,
    UNIQUE(id_revision_clave, numero_pregunta),
    FOREIGN KEY(id_revision_clave, id_version_examen)
      REFERENCES revisiones_clave(id_revision_clave, id_version_examen),
    FOREIGN KEY(id_version_examen, numero_pregunta, id_version_pregunta)
      REFERENCES examen_preguntas(id_version_examen, numero_pregunta, id_version_pregunta),

    CHECK (respuesta_correcta IN ('A','B','C','D','E')),
    FOREIGN KEY(id_version_pregunta, respuesta_correcta)
      REFERENCES alternativas_pregunta(id_version, letra),
    FOREIGN KEY(id_version_examen)
    REFERENCES versiones_examen(id_version),

    FOREIGN KEY(id_version_pregunta)
    REFERENCES pregunta_versiones(id_version)

) ENGINE=InnoDB;

-- ============================================
-- CONFIGURACION DE PUNTAJE
-- Permite penalizacion opcional
-- ============================================

CREATE TABLE configuracion_puntaje (

    id_configuracion INT AUTO_INCREMENT PRIMARY KEY,

    id_examen INT NOT NULL,
    numero_revision INT NOT NULL,
    estado ENUM('BORRADOR','CONFIRMADA') NOT NULL DEFAULT 'BORRADOR',
    creada_por INT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    motivo TEXT NOT NULL,
    UNIQUE(id_examen, numero_revision),
    UNIQUE(id_configuracion, id_examen),
    FOREIGN KEY(creada_por) REFERENCES usuarios(id_usuario),

    puntaje_incorrecta DECIMAL(24,9) NOT NULL DEFAULT 0,

    puntaje_blanco DECIMAL(24,9) NOT NULL DEFAULT 0,

    usa_penalizacion BOOLEAN NOT NULL DEFAULT FALSE,
    CHECK (numero_revision > 0 AND CHAR_LENGTH(TRIM(motivo)) > 0),
    CHECK (puntaje_blanco = 0),
    CHECK ((usa_penalizacion = 0 AND puntaje_incorrecta = 0)
        OR (usa_penalizacion = 1 AND puntaje_incorrecta < 0)),

    FOREIGN KEY(id_examen)
    REFERENCES examenes(id_examen)

) ENGINE=InnoDB;

-- ============================================
-- HISTORIAL DE CAMBIOS DE CONFIGURACION
-- El coordinador puede cambiar pesos cada año
-- ============================================

CREATE TABLE historial_configuracion_examen (

    id_historial INT AUTO_INCREMENT PRIMARY KEY,

    id_examen INT NOT NULL,

    usuario_modifico INT NOT NULL,

    descripcion_cambio TEXT,

    fecha_cambio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(id_examen)
    REFERENCES examenes(id_examen),

    FOREIGN KEY(usuario_modifico)
    REFERENCES usuarios(id_usuario)

) ENGINE=InnoDB;

USE sistema_evaluacion;

-- ============================================
-- BLOQUE 6
-- CARTILLAS, OPEN CV, RESPUESTAS Y RESULTADOS
-- ============================================

-- ============================================
-- CARTILLAS DE RESPUESTAS
-- Una cartilla física pertenece a un estudiante
-- Representa la participación real del estudiante
-- ============================================

-- Nace al recibir la primera cartilla: NO es una inscripción previa.
-- La clave única impide participar en dos áreas de un mismo simulacro.
CREATE TABLE participaciones (
    id_participacion INT AUTO_INCREMENT PRIMARY KEY,
    id_estudiante INT NOT NULL,
    id_simulacro INT NOT NULL,
    id_examen INT NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(id_estudiante, id_simulacro),
    UNIQUE(id_participacion, id_estudiante, id_examen),
    UNIQUE(id_participacion, id_examen),
    FOREIGN KEY(id_estudiante) REFERENCES estudiantes(id_estudiante),
    FOREIGN KEY(id_examen, id_simulacro) REFERENCES examenes(id_examen, id_simulacro)
) ENGINE=InnoDB;

CREATE TABLE cartillas (

    id_cartilla INT AUTO_INCREMENT PRIMARY KEY,
    id_participacion INT NOT NULL,
    numero_recepcion INT NOT NULL,
    vigente BOOLEAN NOT NULL DEFAULT TRUE,
    vigente_unica TINYINT GENERATED ALWAYS AS (IF(vigente, 1, NULL)) STORED,
    reemplaza_cartilla INT NULL,
    motivo_reemplazo TEXT NULL,
    UNIQUE(id_participacion, numero_recepcion),
    UNIQUE(id_participacion, vigente_unica),
    UNIQUE(id_cartilla, id_participacion),
    UNIQUE(id_cartilla, id_estudiante, id_examen, id_version),
    CHECK (numero_recepcion > 0),
    CHECK ((reemplaza_cartilla IS NULL AND numero_recepcion = 1)
        OR (reemplaza_cartilla IS NOT NULL AND numero_recepcion > 1
            AND motivo_reemplazo IS NOT NULL AND CHAR_LENGTH(TRIM(motivo_reemplazo)) > 0)),
    FOREIGN KEY(reemplaza_cartilla, id_participacion) REFERENCES cartillas(id_cartilla, id_participacion),
    FOREIGN KEY(id_participacion, id_estudiante, id_examen)
      REFERENCES participaciones(id_participacion, id_estudiante, id_examen),
    FOREIGN KEY(id_version, id_examen) REFERENCES versiones_examen(id_version, id_examen),

    id_estudiante INT NOT NULL,

    id_examen INT NOT NULL,

    id_version INT NOT NULL,

    codigo_cartilla VARCHAR(50),

    archivo_imagen VARCHAR(255),

    fecha_recepcion DATE,

    operador_recepcion INT,

    observacion TEXT,

    estado ENUM(
        'REGISTRADA',
        'PROCESADA',
        'OBSERVADA',
        'VALIDADA',
        'ANULADA'
    ) DEFAULT 'REGISTRADA',

    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(id_estudiante)
    REFERENCES estudiantes(id_estudiante),

    FOREIGN KEY(id_examen)
    REFERENCES examenes(id_examen),

    FOREIGN KEY(id_version)
    REFERENCES versiones_examen(id_version),

    FOREIGN KEY(operador_recepcion)
    REFERENCES usuarios(id_usuario)

) ENGINE=InnoDB;

-- ============================================
-- HISTORIAL DE PROCESAMIENTO DE CARTILLA
-- Permite reprocesar una misma cartilla
-- ============================================

CREATE TABLE procesamiento_cartilla (

    id_procesamiento INT AUTO_INCREMENT PRIMARY KEY,

    id_cartilla INT NOT NULL,

    numero_intento INT NOT NULL,
    UNIQUE(id_cartilla, numero_intento),
    UNIQUE(id_procesamiento, id_cartilla),
    CHECK (numero_intento > 0),

    metodo ENUM(
        'OPEN_CV',
        'CSV',
        'EXCEL',
        'MANUAL'
    ) NOT NULL,

    usuario_proceso INT,

    fecha_proceso TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    resultado ENUM(
        'EXITOSO',
        'ERROR',
        'REQUIERE_REVISION'
    ),

    observacion TEXT,

    FOREIGN KEY(id_cartilla)
    REFERENCES cartillas(id_cartilla),

    FOREIGN KEY(usuario_proceso)
    REFERENCES usuarios(id_usuario)

) ENGINE=InnoDB;

-- ============================================
-- RESPUESTAS DETECTADAS POR OPEN CV
-- Guarda la lectura original
-- ============================================

CREATE TABLE respuestas_detectadas (

    id_respuesta_detectada INT AUTO_INCREMENT PRIMARY KEY,

    id_cartilla INT NOT NULL,

    id_procesamiento INT NOT NULL,

    numero_pregunta INT NOT NULL,

    respuesta_detectada VARCHAR(5),

    nivel_confianza DECIMAL(5,2),

    requiere_revision BOOLEAN GENERATED ALWAYS AS
      (nivel_confianza IS NULL OR nivel_confianza < 80 OR CHAR_LENGTH(COALESCE(respuesta_detectada, '')) > 1) STORED,
    CHECK (nivel_confianza IS NULL OR (nivel_confianza >= 0 AND nivel_confianza <= 100)),
    CHECK (numero_pregunta > 0),
    FOREIGN KEY(id_procesamiento, id_cartilla)
      REFERENCES procesamiento_cartilla(id_procesamiento, id_cartilla),

    UNIQUE(id_procesamiento, numero_pregunta),
    CHECK (respuesta_detectada IS NULL OR respuesta_detectada REGEXP '^[A-E]{1,5}$'),
    FOREIGN KEY(id_cartilla)
    REFERENCES cartillas(id_cartilla),

    FOREIGN KEY(id_procesamiento)
    REFERENCES procesamiento_cartilla(id_procesamiento)

) ENGINE=InnoDB;

-- ============================================
-- CORRECCIONES MANUALES
-- Cuando el coordinador corrige una lectura
-- ============================================

CREATE TABLE correcciones_manual (

    id_correccion INT AUTO_INCREMENT PRIMARY KEY,

    id_respuesta_detectada INT NOT NULL,

    respuesta_anterior VARCHAR(5),

    respuesta_nueva CHAR(1),
    resolucion ENUM('MARCA_UNICA','BLANCO','MULTIPLE_CONFIRMADA') NOT NULL,
    CHECK ((resolucion = 'MARCA_UNICA' AND respuesta_nueva IS NOT NULL)
        OR (resolucion IN ('BLANCO','MULTIPLE_CONFIRMADA') AND respuesta_nueva IS NULL)),

    usuario_correccion INT NOT NULL,

    motivo TEXT NOT NULL,
    CHECK (CHAR_LENGTH(TRIM(motivo)) > 0),

    fecha_correccion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CHECK (respuesta_anterior IS NULL OR respuesta_anterior REGEXP '^[A-E]{1,5}$'),
    CHECK (respuesta_nueva IS NULL OR respuesta_nueva IN ('A','B','C','D','E')),
    FOREIGN KEY(id_respuesta_detectada)
    REFERENCES respuestas_detectadas(id_respuesta_detectada),

    FOREIGN KEY(usuario_correccion)
    REFERENCES usuarios(id_usuario)

) ENGINE=InnoDB;

-- ============================================
-- RESULTADO DEL EXAMEN DEL ESTUDIANTE
-- ============================================

CREATE TABLE resultados_examen (

    id_resultado INT AUTO_INCREMENT PRIMARY KEY,
    id_revision_clave INT NOT NULL,
    id_configuracion INT NOT NULL,
    calculado_por INT NOT NULL,
    revisado_por INT NULL,
    fecha_revision DATETIME NULL,
    FOREIGN KEY(calculado_por) REFERENCES usuarios(id_usuario),
    FOREIGN KEY(revisado_por) REFERENCES usuarios(id_usuario),
    FOREIGN KEY(id_revision_clave, id_version) REFERENCES revisiones_clave(id_revision_clave, id_version_examen),
    FOREIGN KEY(id_configuracion, id_examen) REFERENCES configuracion_puntaje(id_configuracion, id_examen),
    FOREIGN KEY(id_cartilla, id_estudiante, id_examen, id_version)
      REFERENCES cartillas(id_cartilla, id_estudiante, id_examen, id_version),
    FOREIGN KEY(id_procesamiento, id_cartilla)
      REFERENCES procesamiento_cartilla(id_procesamiento, id_cartilla),
    UNIQUE(id_resultado, id_examen),
    UNIQUE(id_resultado, id_version),
    CHECK (respuestas_correctas >= 0 AND respuestas_incorrectas >= 0 AND respuestas_blanco >= 0),

    id_estudiante INT NOT NULL,

    id_examen INT NOT NULL,

    id_version INT NOT NULL,

    id_cartilla INT NOT NULL,

    respuestas_correctas INT NOT NULL DEFAULT 0,

    respuestas_incorrectas INT NOT NULL DEFAULT 0,

    respuestas_blanco INT NOT NULL DEFAULT 0,

    id_procesamiento INT NOT NULL,

    puntaje_obtenido DECIMAL(24,9) NOT NULL,

    -- Se deriva de puntaje / máximo al consultar; no se guarda un porcentaje redondeado.

    estado ENUM(
        'CALCULADO',
        'REVISADO',
        'PUBLICADO'
    ) DEFAULT 'CALCULADO',

    fecha_calculo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    numero_calculo INT NOT NULL DEFAULT 1,
    vigente BOOLEAN NOT NULL DEFAULT TRUE,
    vigente_unico TINYINT GENERATED ALWAYS AS (IF(vigente, 1, NULL)) STORED,
    UNIQUE(id_estudiante, id_examen, numero_calculo),
    UNIQUE(id_estudiante, id_examen, vigente_unico),
    FOREIGN KEY(id_estudiante)
    REFERENCES estudiantes(id_estudiante),
    FOREIGN KEY(id_examen)
    REFERENCES examenes(id_examen),
    FOREIGN KEY(id_version)
    REFERENCES versiones_examen(id_version),
    FOREIGN KEY(id_cartilla)
    REFERENCES cartillas(id_cartilla),

    FOREIGN KEY(id_procesamiento)
    REFERENCES procesamiento_cartilla(id_procesamiento)

) ENGINE=InnoDB;

-- ============================================
-- DETALLE DE RESPUESTAS DEL RESULTADO
-- Permite mostrar al estudiante:
-- pregunta
-- marcada
-- correcta
-- resultado
-- ============================================

CREATE TABLE publicaciones_examen (
    id_publicacion INT AUTO_INCREMENT PRIMARY KEY,
    id_examen INT NOT NULL,
    numero_publicacion INT NOT NULL,
    publicada_por INT NOT NULL,
    fecha_publicacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    vigente BOOLEAN NOT NULL DEFAULT TRUE,
    vigente_unica TINYINT GENERATED ALWAYS AS (IF(vigente, 1, NULL)) STORED,
    UNIQUE(id_examen, numero_publicacion),
    UNIQUE(id_examen, vigente_unica),
    UNIQUE(id_publicacion, id_examen),
    CHECK (numero_publicacion > 0),
    FOREIGN KEY(id_examen) REFERENCES examenes(id_examen),
    FOREIGN KEY(publicada_por) REFERENCES usuarios(id_usuario)
) ENGINE=InnoDB;

CREATE TABLE publicacion_resultados (
    id_publicacion INT NOT NULL,
    id_examen INT NOT NULL,
    id_resultado INT NOT NULL,
    posicion INT NOT NULL,
    PRIMARY KEY(id_publicacion, id_resultado),
    CHECK (posicion > 0),
    FOREIGN KEY(id_publicacion, id_examen) REFERENCES publicaciones_examen(id_publicacion, id_examen),
    FOREIGN KEY(id_resultado, id_examen) REFERENCES resultados_examen(id_resultado, id_examen)
) ENGINE=InnoDB;

CREATE TABLE detalle_resultado (

    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_respuesta_detectada INT NOT NULL,
    id_correccion_aplicada INT NULL,
    FOREIGN KEY(id_respuesta_detectada) REFERENCES respuestas_detectadas(id_respuesta_detectada),
    FOREIGN KEY(id_correccion_aplicada) REFERENCES correcciones_manual(id_correccion),
    id_examen_pregunta INT NOT NULL,
    id_version_examen INT NOT NULL,
    tipo_respuesta ENUM('UNICA','BLANCO','MULTIPLE_CONFIRMADA') NOT NULL,
    UNIQUE(id_resultado, id_examen_pregunta),
    FOREIGN KEY(id_resultado, id_version_examen) REFERENCES resultados_examen(id_resultado, id_version),
    FOREIGN KEY(id_examen_pregunta, id_version_examen, id_version_pregunta)
      REFERENCES examen_preguntas(id_examen_pregunta, id_version_examen, id_version_pregunta),
    CHECK ((tipo_respuesta = 'UNICA' AND respuesta_marcada IS NOT NULL)
      OR (tipo_respuesta IN ('BLANCO','MULTIPLE_CONFIRMADA') AND respuesta_marcada IS NULL)),
    CHECK (tipo_respuesta = 'UNICA' OR (puntaje_obtenido = 0 AND es_correcta = 0)),

    id_resultado INT NOT NULL,

    id_version_pregunta INT NOT NULL,

    respuesta_marcada CHAR(1),

    respuesta_correcta CHAR(1),

    es_correcta BOOLEAN NOT NULL,

    puntaje_obtenido DECIMAL(24,9) NOT NULL,

    CHECK (respuesta_marcada IS NULL OR respuesta_marcada IN ('A','B','C','D','E')),
    CHECK (respuesta_correcta IS NULL OR respuesta_correcta IN ('A','B','C','D','E')),
    FOREIGN KEY(id_resultado)
    REFERENCES resultados_examen(id_resultado),

    FOREIGN KEY(id_version_pregunta)
    REFERENCES pregunta_versiones(id_version)

) ENGINE=InnoDB;

-- ============================================
-- RESULTADO POR MATERIA
-- Para ver:
-- Matemática
-- Física
-- Comunicación
-- ============================================

CREATE TABLE resultado_materia (

    id_resultado_materia INT AUTO_INCREMENT PRIMARY KEY,

    id_resultado INT NOT NULL,

    id_materia INT NOT NULL,

    preguntas_total INT,

    correctas INT,

    incorrectas INT,

    blanco INT,

    puntaje DECIMAL(24,9),

    UNIQUE(id_resultado, id_materia),

    FOREIGN KEY(id_resultado)
    REFERENCES resultados_examen(id_resultado),

    FOREIGN KEY(id_materia)
    REFERENCES materias(id_materia)

) ENGINE=InnoDB;

USE sistema_evaluacion;

USE sistema_evaluacion;

-- ============================================
-- CABECERA DEL RANKING
-- Guarda cada proceso de generación
-- ============================================


USE sistema_evaluacion;

-- ============================================
-- BLOQUE 9
-- REPORTES Y ESTADISTICAS INSTITUCIONALES
-- ============================================

-- ============================================
-- TIPOS DE REPORTES
-- ============================================

CREATE TABLE tipos_reporte (

    id_tipo_reporte INT AUTO_INCREMENT PRIMARY KEY,

    nombre VARCHAR(100) NOT NULL,

    descripcion VARCHAR(255)

) ENGINE=InnoDB;

INSERT INTO tipos_reporte(nombre,descripcion)
VALUES

('REPORTE_ESTUDIANTE',
'Reporte individual del rendimiento del estudiante'),

('REPORTE_AREA',
'Reporte estadístico por área académica'),

('REPORTE_MATERIA',
'Reporte por materia'),

('REPORTE_EXAMEN',
'Reporte de resultados de un examen'),

('REPORTE_INSTITUCIONAL',
'Reporte general para dirección');

-- ============================================
-- REPORTES GENERADOS
-- PDF / EXCEL
-- ============================================

CREATE TABLE reportes (

    id_reporte INT AUTO_INCREMENT PRIMARY KEY,

    id_tipo_reporte INT NOT NULL,

    generado_por INT NOT NULL,

    titulo VARCHAR(200),

    formato ENUM(
        'PDF',
        'EXCEL'
    ) NOT NULL,

    ruta_archivo VARCHAR(255),

    fecha_generacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    estado ENUM(
        'GENERADO',
        'ERROR'
    ) DEFAULT 'GENERADO',

    FOREIGN KEY(id_tipo_reporte)
    REFERENCES tipos_reporte(id_tipo_reporte),

    FOREIGN KEY(generado_por)
    REFERENCES usuarios(id_usuario)

) ENGINE=InnoDB;

USE sistema_evaluacion;

-- ============================================
-- BLOQUE 10
-- INDICES, VISTAS, TRIGGERS Y DATOS INICIALES
-- ============================================

CREATE TABLE pregunta_areas (
    id_pregunta INT NOT NULL,
    id_area INT NOT NULL,
    PRIMARY KEY(
        id_pregunta,
        id_area
    ),
    FOREIGN KEY(id_pregunta)
    REFERENCES preguntas(id_pregunta),
    FOREIGN KEY(id_area)
    REFERENCES areas(id_area)
) ENGINE=InnoDB;

-- ============================================
-- INDICES PARA OPTIMIZACION
-- ============================================

CREATE INDEX idx_estudiante_codigo
ON estudiantes(codigo_estudiante);

CREATE INDEX idx_usuario_username
ON usuarios(username);

CREATE INDEX idx_pregunta_materia
ON preguntas(id_materia);

CREATE INDEX idx_pregunta_estado
ON preguntas(estado);

CREATE INDEX idx_examen_fecha
ON examenes(fecha_programada);

CREATE INDEX idx_resultado_estudiante
ON resultados_examen(id_estudiante);

CREATE INDEX idx_resultado_examen
ON resultados_examen(id_examen);

CREATE INDEX idx_cartilla_estudiante
ON cartillas(id_estudiante);

CREATE INDEX idx_materia_eje
ON materias(id_eje);

CREATE INDEX idx_area_nombre
ON areas(nombre);

-- ============================================
-- VISTAS PARA CONSULTAS FRECUENTES
-- ============================================

-- ============================================
-- Vista resultados del estudiante
-- ============================================

CREATE VIEW vw_resultados_publicados AS
SELECT r.*, p.id_publicacion, p.fecha_publicacion, p.publicada_por, pr.posicion,
    r.puntaje_obtenido * 100 / ex.puntaje_total AS porcentaje
FROM publicaciones_examen p
INNER JOIN publicacion_resultados pr ON pr.id_publicacion = p.id_publicacion
INNER JOIN resultados_examen r ON r.id_resultado = pr.id_resultado
INNER JOIN examenes ex ON ex.id_examen = r.id_examen
WHERE p.vigente = 1 AND r.estado = 'PUBLICADO';

CREATE VIEW vw_resultados_estudiante AS

SELECT

    r.id_estudiante,
    e.codigo_estudiante,

    CONCAT(e.nombres,' ',e.apellidos)
    AS estudiante,

    ex.nombre
    AS examen,

    r.puntaje_obtenido,

    r.respuestas_correctas,

    r.respuestas_incorrectas,

    r.respuestas_blanco,

    r.fecha_calculo, r.fecha_publicacion

FROM vw_resultados_publicados r

INNER JOIN estudiantes e
ON r.id_estudiante = e.id_estudiante

INNER JOIN examenes ex
ON r.id_examen = ex.id_examen

WHERE r.estado = 'PUBLICADO';

-- ============================================
-- Vista banco preguntas aprobadas
-- Trae el enunciado desde la version activa
-- ============================================

CREATE VIEW vw_banco_preguntas_activo AS
SELECT
    p.id_pregunta,
    pv.enunciado,
    et.nombre AS eje,
    m.nombre AS materia,
    GROUP_CONCAT(a.nombre ORDER BY a.nombre SEPARATOR ', ') AS areas
FROM preguntas p
INNER JOIN pregunta_versiones pv
ON pv.id_pregunta = p.id_pregunta
AND pv.estado = 'ACTIVA' AND pv.sellada = 1
INNER JOIN materias m
ON p.id_materia = m.id_materia
INNER JOIN ejes_tematicos et
ON m.id_eje = et.id_eje
LEFT JOIN pregunta_areas pa
ON pa.id_pregunta = p.id_pregunta
LEFT JOIN areas a
ON pa.id_area = a.id_area
WHERE p.estado='APROBADA'
GROUP BY p.id_pregunta, pv.enunciado, et.nombre, m.nombre;

-- ============================================
-- Actualizar estado de pregunta
-- cuando coordinador aprueba
-- ============================================

DELIMITER $$

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

DELIMITER ;

-- ============================================
-- DATOS INICIALES
-- AREAS
-- ============================================

INSERT INTO areas
(
codigo,
nombre,
descripcion
)

VALUES

(
'ING',
'Ingenierías',
'Área orientada a carreras de ingeniería'
),

(
'BIO',
'Biomédicas',
'Área ciencias de la salud'
),

(
'SOC',
'Sociales',
'Área ciencias sociales'
);

-- ============================================
-- EJES TEMATICOS BASE
-- ============================================

INSERT INTO ejes_tematicos
(
nombre,
descripcion
)
VALUES
(
'Matemática',
'Área matemática'
),
(
'Comunicación',
'Lenguaje y comprensión lectora'
),
(
'Ciencias',
'Física química biología'
);

-- ============================================
-- DATOS CICLOS
-- ============================================

INSERT INTO ciclos_preparacion
(
nombre,
fecha_inicio,
fecha_fin
)

VALUES

(
'PRE 2026-I',
'2026-01-01',
'2026-06-30'
);

-- ============================================
-- FIN DEL SCRIPT BASE
-- ============================================

USE sistema_evaluacion;

USE sistema_evaluacion;

DELIMITER $$

CREATE TRIGGER trg_estudiante_un_solo_rol
BEFORE INSERT ON usuario_roles
FOR EACH ROW
BEGIN
DECLARE v_rol_estudiante INT;
DECLARE v_total_roles INT;
DECLARE v_es_estudiante INT;
SELECT id_rol INTO v_rol_estudiante
FROM roles
WHERE nombre = 'ESTUDIANTE';
SELECT COUNT(*) INTO v_total_roles
FROM usuario_roles
WHERE id_usuario = NEW.id_usuario;
SELECT COUNT(*) INTO v_es_estudiante
FROM usuario_roles
WHERE id_usuario = NEW.id_usuario
AND id_rol = v_rol_estudiante;
IF (NEW.id_rol = v_rol_estudiante AND v_total_roles > 0)
OR (NEW.id_rol <> v_rol_estudiante AND v_es_estudiante > 0)
THEN
SIGNAL SQLSTATE '45000'
SET MESSAGE_TEXT = 'Un estudiante solo puede tener el rol ESTUDIANTE';
END IF;
END$$

DELIMITER ;

USE sistema_evaluacion;

CREATE TABLE pregunta_imagenes (
    id_imagen INT AUTO_INCREMENT PRIMARY KEY,
    id_version INT NOT NULL,
    ubicacion ENUM(
        'ENUNCIADO',
        'ALTERNATIVA'
    ) NOT NULL DEFAULT 'ENUNCIADO',
    letra CHAR(1) NULL,
    orden INT DEFAULT 1,
    ruta_archivo VARCHAR(255) NOT NULL,
    tipo_archivo VARCHAR(50),
    tamano_kb INT,
    texto_alternativo VARCHAR(255),
    subido_por INT,
    fecha_subida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CHECK (
        (ubicacion = 'ENUNCIADO' AND letra IS NULL)
        OR (ubicacion = 'ALTERNATIVA' AND letra IS NOT NULL)
    ),
    FOREIGN KEY(id_version)
    REFERENCES pregunta_versiones(id_version),
    FOREIGN KEY(id_version, letra)
    REFERENCES alternativas_pregunta(id_version, letra),
    FOREIGN KEY(subido_por)
    REFERENCES usuarios(id_usuario)
) ENGINE=InnoDB;

CREATE INDEX idx_imagen_version
ON pregunta_imagenes(id_version);

USE sistema_evaluacion;

DELIMITER $$

CREATE TRIGGER trg_examen_pregunta_valida
BEFORE INSERT ON examen_preguntas
FOR EACH ROW
BEGIN
DECLARE v_pregunta INT;
DECLARE v_estado VARCHAR(20);
DECLARE v_area INT;
DECLARE v_ok INT;
SELECT p.id_pregunta, p.estado
INTO v_pregunta, v_estado
FROM pregunta_versiones pv
INNER JOIN preguntas p
ON p.id_pregunta = pv.id_pregunta
WHERE pv.id_version = NEW.id_version_pregunta AND pv.sellada = 1 AND pv.estado = 'ACTIVA';
IF v_estado IS NULL OR v_estado <> 'APROBADA' THEN
SIGNAL SQLSTATE '45000'
SET MESSAGE_TEXT = 'Solo se pueden usar preguntas APROBADAS en un examen';
END IF;
SELECT ex.id_area INTO v_area
FROM versiones_examen ve
INNER JOIN examenes ex
ON ex.id_examen = ve.id_examen
WHERE ve.id_version = NEW.id_version_examen;
SELECT COUNT(*) INTO v_ok
FROM pregunta_areas
WHERE id_pregunta = v_pregunta
AND id_area = v_area;
IF v_ok = 0 THEN
SIGNAL SQLSTATE '45000'
SET MESSAGE_TEXT = 'La pregunta no esta marcada para el area del examen';
END IF;
END$$

CREATE TRIGGER trg_examen_aprobado_valida
BEFORE UPDATE ON examenes
FOR EACH ROW
BEGIN
    IF NEW.estado = 'APROBADO' AND OLD.estado <> 'APROBADO' THEN
        IF COALESCE((SELECT SUM(peso_porcentaje) FROM examen_ejes WHERE id_examen = NEW.id_examen), 0) <> 100
          OR COALESCE((SELECT SUM(puntaje_asignado) FROM distribucion_examen WHERE id_examen = NEW.id_examen), 0) <> NEW.puntaje_total THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Pesos y puntajes deben coincidir exactamente; no se redondea';
        END IF;
        IF EXISTS (SELECT 1 FROM examen_ejes ee WHERE ee.id_examen = NEW.id_examen
            AND COALESCE((SELECT SUM(d.puntaje_asignado) FROM distribucion_examen d
                INNER JOIN materias m ON m.id_materia = d.id_materia
                WHERE d.id_examen = ee.id_examen AND m.id_eje = ee.id_eje), 0) * 100
                <> NEW.puntaje_total * ee.peso_porcentaje)
          OR EXISTS (SELECT 1 FROM distribucion_examen d INNER JOIN materias m ON m.id_materia = d.id_materia
            WHERE d.id_examen = NEW.id_examen AND NOT EXISTS
                (SELECT 1 FROM examen_ejes ee WHERE ee.id_examen = d.id_examen AND ee.id_eje = m.id_eje)) THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El puntaje de cada eje debe corresponder a su peso';
        END IF;
        IF NOT EXISTS (SELECT 1 FROM versiones_examen WHERE id_examen = NEW.id_examen AND estado = 'ACTIVA')
          OR EXISTS (SELECT 1 FROM versiones_examen v CROSS JOIN distribucion_examen d
            WHERE v.id_examen = NEW.id_examen AND d.id_examen = NEW.id_examen AND v.estado = 'ACTIVA'
            AND d.cantidad_preguntas <> (SELECT COUNT(*) FROM examen_preguntas ep
                INNER JOIN pregunta_versiones pv ON pv.id_version = ep.id_version_pregunta
                INNER JOIN preguntas p ON p.id_pregunta = pv.id_pregunta
                WHERE ep.id_version_examen = v.id_version AND p.id_materia = d.id_materia))
          OR EXISTS (SELECT 1 FROM examen_preguntas ep
            INNER JOIN versiones_examen v ON v.id_version = ep.id_version_examen
            INNER JOIN pregunta_versiones pv ON pv.id_version = ep.id_version_pregunta
            INNER JOIN preguntas p ON p.id_pregunta = pv.id_pregunta
            LEFT JOIN distribucion_examen d ON d.id_examen = v.id_examen AND d.id_materia = p.id_materia
            WHERE v.id_examen = NEW.id_examen AND v.estado = 'ACTIVA'
              AND (d.id_distribucion IS NULL OR ep.puntaje <> d.puntaje_por_pregunta)) THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cada version debe cumplir cantidades y puntajes por materia';
        END IF;
        IF EXISTS (SELECT 1 FROM versiones_examen a
            INNER JOIN versiones_examen b ON b.id_examen = a.id_examen AND b.estado = 'ACTIVA'
            INNER JOIN examen_preguntas ep ON ep.id_version_examen = a.id_version
            WHERE a.id_examen = NEW.id_examen AND a.estado = 'ACTIVA'
              AND NOT EXISTS (SELECT 1 FROM examen_preguntas bp
                WHERE bp.id_version_examen = b.id_version AND bp.id_version_pregunta = ep.id_version_pregunta)) THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'A y B deben contener las mismas versiones de preguntas';
        END IF;
        IF EXISTS (SELECT 1 FROM versiones_examen v WHERE v.id_examen = NEW.id_examen AND v.estado = 'ACTIVA'
            AND ((SELECT MIN(numero_pregunta) FROM examen_preguntas WHERE id_version_examen = v.id_version) <> 1
              OR (SELECT MAX(numero_pregunta) FROM examen_preguntas WHERE id_version_examen = v.id_version)
                 <> (SELECT COUNT(*) FROM examen_preguntas WHERE id_version_examen = v.id_version))) THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La numeracion de preguntas debe ser consecutiva desde 1';
        END IF;
    END IF;
    IF OLD.estado IN ('APROBADO','APLICADO','CERRADO') AND
       (NEW.id_area <> OLD.id_area OR NEW.id_simulacro <> OLD.id_simulacro OR NEW.puntaje_total <> OLD.puntaje_total
        OR NOT (NEW.fecha_programada <=> OLD.fecha_programada)
        OR NEW.estado IN ('BORRADOR','CONFIGURACION')) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La estructura aprobada del examen es inmutable';
    END IF;
END$$

DELIMITER ;

USE sistema_evaluacion;

-- ============================================
-- RANKINGS, ESTADISTICAS, PERFIL Y PROGRESO
-- El ranking se conserva por publicación; las estadísticas se derivan de los
-- resultados de la publicación vigente. Umbrales de dificultad: propuestos.
-- ============================================

CREATE VIEW vw_ranking_examen AS
SELECT r.id_examen, ex.id_simulacro, ex.id_area, sim.id_ciclo, r.id_estudiante,
    e.codigo_estudiante, CONCAT(e.nombres,' ',e.apellidos) AS estudiante,
    r.puntaje_obtenido AS puntaje, r.porcentaje,
    r.respuestas_correctas AS aciertos, r.respuestas_incorrectas AS errores,
    r.respuestas_blanco AS en_blanco,
    (r.respuestas_correctas + r.respuestas_incorrectas + r.respuestas_blanco) AS total_preguntas,
    r.posicion AS posicion
FROM vw_resultados_publicados r
INNER JOIN examenes ex ON ex.id_examen = r.id_examen
INNER JOIN simulacros sim ON sim.id_simulacro = ex.id_simulacro
INNER JOIN estudiantes e ON e.id_estudiante = r.id_estudiante
WHERE r.estado = 'PUBLICADO';

CREATE VIEW vw_ranking_area AS
SELECT * FROM vw_ranking_examen;

-- El ranking por área es el del examen de esa área en el simulacro.
-- No se genera ranking general cruzando áreas o fechas.
CREATE VIEW vw_ranking_materia AS
SELECT r.id_examen, rm.id_materia, r.id_estudiante, e.codigo_estudiante,
    CONCAT(e.nombres,' ',e.apellidos) AS estudiante, rm.puntaje,
    RANK() OVER (PARTITION BY r.id_examen, rm.id_materia ORDER BY rm.puntaje DESC) AS posicion
FROM resultado_materia rm
INNER JOIN vw_resultados_publicados r ON r.id_resultado = rm.id_resultado
INNER JOIN estudiantes e ON e.id_estudiante = r.id_estudiante
WHERE r.estado = 'PUBLICADO';

CREATE VIEW vw_evolucion_estudiante AS
SELECT r.id_estudiante, r.id_examen, ex.nombre AS examen, ex.fecha_programada AS fecha,
    r.puntaje_obtenido AS puntaje, r.porcentaje, rk.posicion AS posicion_ranking
FROM vw_resultados_publicados r
INNER JOIN examenes ex ON ex.id_examen = r.id_examen
INNER JOIN vw_ranking_examen rk ON rk.id_examen = r.id_examen AND rk.id_estudiante = r.id_estudiante
WHERE r.estado = 'PUBLICADO';

CREATE VIEW vw_progreso_estudiante AS
SELECT e.id_estudiante, e.codigo_estudiante, CONCAT(e.nombres,' ',e.apellidos) AS estudiante,
    COUNT(r.id_resultado) AS total_examenes,
    AVG(r.porcentaje) AS promedio_porcentaje,
    MAX(r.porcentaje) AS mejor_porcentaje,
    COALESCE(SUM(r.respuestas_correctas), 0) AS total_aciertos,
    COALESCE(SUM(r.respuestas_incorrectas), 0) AS total_errores,
    COALESCE(SUM(r.respuestas_blanco), 0) AS total_blancos
FROM estudiantes e
LEFT JOIN vw_resultados_publicados r ON r.id_estudiante = e.id_estudiante AND r.estado = 'PUBLICADO'
GROUP BY e.id_estudiante, e.codigo_estudiante, e.nombres, e.apellidos;

CREATE VIEW vw_progreso_materia_estudiante AS
SELECT r.id_estudiante, r.id_examen, rm.id_materia, rm.preguntas_total,
    rm.correctas, rm.incorrectas, rm.blanco,
    rm.correctas * 100 / NULLIF(rm.preguntas_total, 0) AS porcentaje
FROM resultado_materia rm
INNER JOIN vw_resultados_publicados r ON r.id_resultado = rm.id_resultado
WHERE r.estado = 'PUBLICADO';

CREATE VIEW vw_progreso_area_estudiante AS
SELECT r.id_estudiante, ex.id_area, COUNT(*) AS total_examenes,
    AVG(r.porcentaje) AS porcentaje_promedio
FROM vw_resultados_publicados r
INNER JOIN examenes ex ON ex.id_examen = r.id_examen
WHERE r.estado = 'PUBLICADO'
GROUP BY r.id_estudiante, ex.id_area;

CREATE VIEW vw_estadisticas_examen AS
SELECT ex.id_examen, ex.id_simulacro, sim.id_ciclo, ex.id_area, COUNT(*) AS participantes,
    AVG(r.puntaje_obtenido) AS promedio,
    MAX(r.puntaje_obtenido) AS mejor_puntaje,
    MIN(r.puntaje_obtenido) AS menor_puntaje
FROM vw_resultados_publicados r
INNER JOIN examenes ex ON ex.id_examen = r.id_examen
INNER JOIN simulacros sim ON sim.id_simulacro = ex.id_simulacro
WHERE r.estado = 'PUBLICADO'
GROUP BY ex.id_examen, ex.id_simulacro, sim.id_ciclo, ex.id_area;

CREATE VIEW vw_estadisticas_generales AS
SELECT
    (SELECT COUNT(DISTINCT id_estudiante) FROM vw_resultados_publicados) AS estudiantes_evaluados,
    (SELECT COUNT(*) FROM estudiantes WHERE estado = 'ACTIVO') AS total_estudiantes,
    (SELECT COUNT(*) FROM docentes) AS total_docentes,
    (SELECT COUNT(*) FROM examenes) AS total_examenes,
    (SELECT AVG(porcentaje) FROM vw_resultados_publicados) AS promedio_porcentaje,
    (SELECT MAX(porcentaje) FROM vw_resultados_publicados) AS porcentaje_maximo,
    (SELECT MIN(porcentaje) FROM vw_resultados_publicados) AS porcentaje_minimo;

CREATE VIEW vw_estadisticas_materia AS
SELECT x.*,
    CASE WHEN x.promedio_aciertos >= 70 THEN 'FACIL'
         WHEN x.promedio_aciertos >= 40 THEN 'MEDIA'
         ELSE 'DIFICIL' END AS dificultad_calculada
FROM (
    SELECT r.id_examen, rm.id_materia, MAX(rm.preguntas_total) AS preguntas_evaluadas,
        AVG(rm.correctas * 100 / NULLIF(rm.preguntas_total, 0)) AS promedio_aciertos,
        AVG(rm.incorrectas * 100 / NULLIF(rm.preguntas_total, 0)) AS porcentaje_error,
        AVG(rm.blanco * 100 / NULLIF(rm.preguntas_total, 0)) AS porcentaje_blanco
    FROM resultado_materia rm
    INNER JOIN vw_resultados_publicados r ON r.id_resultado = rm.id_resultado
    WHERE r.estado = 'PUBLICADO'
    GROUP BY r.id_examen, rm.id_materia
) x;

CREATE VIEW vw_estadisticas_grupo AS
SELECT h.id_grupo, r.id_examen, COUNT(*) AS cantidad_participantes,
    AVG(r.puntaje_obtenido) AS promedio_grupo,
    MAX(r.puntaje_obtenido) AS mejor_puntaje,
    MIN(r.puntaje_obtenido) AS menor_puntaje
FROM vw_resultados_publicados r
INNER JOIN examenes ex ON ex.id_examen = r.id_examen
INNER JOIN estudiante_grupo_historial h
    ON h.id_estudiante = r.id_estudiante
    AND ex.fecha_programada >= h.fecha_inicio
    AND (h.fecha_fin IS NULL OR ex.fecha_programada < h.fecha_fin)
INNER JOIN grupos_academicos g ON g.id_grupo = h.id_grupo
INNER JOIN simulacros sim ON sim.id_simulacro = ex.id_simulacro AND sim.id_ciclo = g.id_ciclo
WHERE r.estado = 'PUBLICADO'
GROUP BY h.id_grupo, r.id_examen;

CREATE VIEW vw_analisis_preguntas AS
SELECT t.*,
    CASE WHEN t.porcentaje_acierto >= 70 THEN 'FACIL'
         WHEN t.porcentaje_acierto >= 40 THEN 'MEDIA'
         ELSE 'DIFICIL' END AS dificultad
FROM (
    SELECT r.id_examen, pv.id_pregunta, COUNT(*) AS veces_respondida,
        SUM(d.es_correcta) AS veces_correcta,
        SUM(d.es_correcta) * 100 / COUNT(*) AS porcentaje_acierto
    FROM detalle_resultado d
    INNER JOIN vw_resultados_publicados r ON r.id_resultado = d.id_resultado
    INNER JOIN pregunta_versiones pv ON pv.id_version = d.id_version_pregunta
    WHERE r.estado = 'PUBLICADO'
    GROUP BY r.id_examen, pv.id_pregunta
) t;

-- ============================================
-- INDICES PARA LAS CONSULTAS ANTERIORES
-- ============================================
CREATE INDEX idx_resultado_examen_estado ON resultados_examen(id_examen, estado, puntaje_obtenido);
CREATE INDEX idx_resultado_estudiante_estado ON resultados_examen(id_estudiante, estado);
CREATE INDEX idx_detalle_pregunta ON detalle_resultado(id_version_pregunta, es_correcta);
CREATE INDEX idx_resultado_materia_materia ON resultado_materia(id_materia, id_resultado);
CREATE INDEX idx_examen_area_simulacro ON examenes(id_area, id_simulacro);
CREATE INDEX idx_simulacro_ciclo ON simulacros(id_ciclo, estado);
CREATE INDEX idx_est_grupo_fechas ON estudiante_grupo_historial(id_estudiante, fecha_inicio, fecha_fin);
CREATE INDEX idx_cartilla_examen_estado ON cartillas(id_examen, estado);
CREATE INDEX idx_pregunta_materia_estado ON preguntas(id_materia, estado);
CREATE INDEX idx_version_pregunta_estado ON pregunta_versiones(id_pregunta, estado);
CREATE INDEX idx_pregunta_area ON pregunta_areas(id_area, id_pregunta);
CREATE INDEX idx_lectura_revision ON respuestas_detectadas(id_cartilla, requiere_revision);

USE sistema_evaluacion;

INSERT INTO permisos(nombre,descripcion)
VALUES
('GESTIONAR_USUARIOS','Registrar usuarios y asignar roles'),
('PUBLICAR_RESULTADOS','Publicar resultados calculados'),
('RECALIFICAR_EXAMEN','Recalificar un examen conservando resultados anteriores'),
('VER_ESTADISTICAS','Consultar estadisticas');

INSERT INTO rol_permisos(id_rol,id_permiso)
SELECT r.id_rol, p.id_permiso
FROM roles r
INNER JOIN permisos p
ON (r.nombre, p.nombre) IN (
('DOCENTE','CREAR_PREGUNTA'),('DOCENTE','EDITAR_PREGUNTA'),('DOCENTE','VER_ESTADISTICAS'),
('COORDINADOR','APROBAR_PREGUNTA'),('COORDINADOR','CREAR_EXAMEN'),('COORDINADOR','CONFIGURAR_EXAMEN'),
('COORDINADOR','PROCESAR_CARTILLA'),('COORDINADOR','CORREGIR_CARTILLA'),('COORDINADOR','PUBLICAR_RESULTADOS'),
('COORDINADOR','RECALIFICAR_EXAMEN'),('COORDINADOR','VER_RESULTADOS'),('COORDINADOR','VER_RANKING'),
('COORDINADOR','VER_ESTADISTICAS'),('COORDINADOR','GENERAR_REPORTES'),('COORDINADOR','GESTIONAR_USUARIOS'),
('ESTUDIANTE','VER_RESULTADOS'),('ESTUDIANTE','VER_PERFIL'),('ESTUDIANTE','VER_RANKING'),
('DIRECTOR','APROBAR_PREGUNTA'),('DIRECTOR','CREAR_EXAMEN'),('DIRECTOR','CONFIGURAR_EXAMEN'),
('DIRECTOR','PROCESAR_CARTILLA'),('DIRECTOR','CORREGIR_CARTILLA'),('DIRECTOR','PUBLICAR_RESULTADOS'),
('DIRECTOR','RECALIFICAR_EXAMEN'),('DIRECTOR','VER_RESULTADOS'),('DIRECTOR','VER_RANKING'),
('DIRECTOR','VER_ESTADISTICAS'),('DIRECTOR','GENERAR_REPORTES'),('DIRECTOR','GESTIONAR_USUARIOS')
);

INSERT INTO rol_paneles(id_rol,id_panel)
SELECT r.id_rol, p.id_panel
FROM roles r
INNER JOIN paneles p
ON (r.nombre, p.nombre) IN (
('DIRECTOR','Panel Director'),('COORDINADOR','Panel Coordinador'),
('DOCENTE','Panel Docente'),('ESTUDIANTE','Panel Estudiante')
);

-- Cuentas de prueba: contraseña provisional compartida "miclave".
INSERT INTO usuarios(username,password_hash,nombres,apellidos,estado)
VALUES
('coordinador','pbkdf2:sha256:1000000$y1UnncYou9CBqWpc$63fa4c1940efbcf4de3c4fc7f259b601bce3c07a63be31a043ffd37064d523e9','Coordinador','Prueba','ACTIVO'),
('director','pbkdf2:sha256:1000000$y1UnncYou9CBqWpc$63fa4c1940efbcf4de3c4fc7f259b601bce3c07a63be31a043ffd37064d523e9','Director','Prueba','ACTIVO'),
('docente','pbkdf2:sha256:1000000$y1UnncYou9CBqWpc$63fa4c1940efbcf4de3c4fc7f259b601bce3c07a63be31a043ffd37064d523e9','Docente','Prueba','ACTIVO'),
('estudiante','pbkdf2:sha256:1000000$y1UnncYou9CBqWpc$63fa4c1940efbcf4de3c4fc7f259b601bce3c07a63be31a043ffd37064d523e9','Estudiante','Prueba','ACTIVO');

INSERT INTO usuario_roles(id_usuario,id_rol)
SELECT u.id_usuario, r.id_rol
FROM usuarios u
INNER JOIN roles r ON r.nombre = UPPER(u.username)
WHERE u.username IN ('coordinador','director','docente','estudiante');

INSERT INTO coordinadores(id_usuario,cargo)
SELECT id_usuario, 'Coordinador académico'
FROM usuarios
WHERE username = 'coordinador';

INSERT INTO directores(id_usuario,cargo)
SELECT id_usuario, 'Director de prueba' FROM usuarios WHERE username = 'director';
INSERT INTO docentes(id_usuario,codigo_docente)
SELECT id_usuario, 'DOC-PRUEBA' FROM usuarios WHERE username = 'docente';
INSERT INTO estudiantes(id_usuario,codigo_estudiante,nombres,apellidos)
SELECT id_usuario, 'EST-PRUEBA', 'Estudiante', 'Prueba' FROM usuarios WHERE username = 'estudiante';

USE sistema_evaluacion;

CREATE VIEW vw_simulacros_resumen AS
SELECT s.id_simulacro, s.id_ciclo, s.nombre, s.fecha, s.estado,
    COUNT(DISTINCT ex.id_examen) AS examenes,
    AVG(r.porcentaje) AS promedio_porcentaje
FROM simulacros s
LEFT JOIN examenes ex ON ex.id_simulacro = s.id_simulacro
LEFT JOIN vw_resultados_publicados r
    ON r.id_examen = ex.id_examen AND r.estado = 'PUBLICADO'
GROUP BY s.id_simulacro, s.id_ciclo, s.nombre, s.fecha, s.estado;

-- OPERACIONES TRANSACCIONALES
-- La aplicación utiliza estas operaciones con el usuario autenticado.
-- No conceder DML directo a clientes finales. Ver criterios del documento 7.
DELIMITER $$

CREATE TRIGGER trg_roles_update
BEFORE UPDATE ON usuario_roles FOR EACH ROW
BEGIN
    IF EXISTS (SELECT 1 FROM usuario_roles ur
        INNER JOIN roles actual ON actual.id_rol = ur.id_rol
        INNER JOIN roles nuevo ON nuevo.id_rol = NEW.id_rol
        WHERE ur.id_usuario = NEW.id_usuario
          AND NOT (ur.id_usuario = OLD.id_usuario AND ur.id_rol = OLD.id_rol)
          AND ((nuevo.nombre = 'ESTUDIANTE' AND actual.nombre <> 'ESTUDIANTE')
            OR (nuevo.nombre <> 'ESTUDIANTE' AND actual.nombre = 'ESTUDIANTE'))) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El rol ESTUDIANTE es exclusivo tambien al actualizar';
    END IF;
END$$

CREATE TRIGGER trg_version_pregunta_sellar
BEFORE UPDATE ON pregunta_versiones FOR EACH ROW
BEGIN
    IF OLD.sellada AND (NEW.id_pregunta <> OLD.id_pregunta OR NEW.numero_version <> OLD.numero_version
      OR NEW.enunciado <> OLD.enunciado OR NEW.respuesta_correcta <> OLD.respuesta_correcta OR NEW.sellada = 0
      OR NOT (NEW.usuario_modifico <=> OLD.usuario_modifico)) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El contenido sellado es inmutable; crear nueva version';
    END IF;
    IF NEW.sellada AND NOT OLD.sellada AND
      ((SELECT COUNT(*) FROM alternativas_pregunta WHERE id_version = NEW.id_version) < 2
       OR NOT EXISTS (SELECT 1 FROM alternativas_pregunta WHERE id_version = NEW.id_version AND letra = NEW.respuesta_correcta)) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La version requiere alternativas y una clave existente';
    END IF;
END$$

CREATE TRIGGER trg_version_pregunta_insert
BEFORE INSERT ON pregunta_versiones FOR EACH ROW
BEGIN
    IF NEW.sellada THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Crear contenido y alternativas antes de sellar';
    END IF;
END$$

CREATE TRIGGER trg_pregunta_materia_inmutable
BEFORE UPDATE ON preguntas FOR EACH ROW
BEGIN
    IF NEW.id_materia <> OLD.id_materia AND EXISTS
       (SELECT 1 FROM pregunta_versiones WHERE id_pregunta = OLD.id_pregunta AND sellada = 1) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No cambiar materia de una pregunta con contenido sellado';
    END IF;
END$$

CREATE TRIGGER trg_clave_confirmar
BEFORE UPDATE ON revisiones_clave FOR EACH ROW
BEGIN
    IF OLD.estado = 'CONFIRMADA' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La revision de clave confirmada es inmutable';
    END IF;
    IF NEW.estado = 'CONFIRMADA' AND
      (SELECT COUNT(*) FROM plantilla_respuestas WHERE id_revision_clave = NEW.id_revision_clave)
      <> (SELECT COUNT(*) FROM examen_preguntas WHERE id_version_examen = NEW.id_version_examen) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La clave debe cubrir todas las posiciones del cuadernillo';
    END IF;
END$$

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

CREATE TRIGGER trg_resultado_update
BEFORE UPDATE ON resultados_examen FOR EACH ROW
BEGIN
    IF NEW.id_estudiante <> OLD.id_estudiante OR NEW.id_examen <> OLD.id_examen
      OR NEW.id_version <> OLD.id_version OR NEW.id_cartilla <> OLD.id_cartilla
      OR NEW.id_procesamiento <> OLD.id_procesamiento OR NEW.id_revision_clave <> OLD.id_revision_clave
      OR NEW.id_configuracion <> OLD.id_configuracion OR NEW.puntaje_obtenido <> OLD.puntaje_obtenido
      OR NEW.respuestas_correctas <> OLD.respuestas_correctas OR NEW.respuestas_incorrectas <> OLD.respuestas_incorrectas
      OR NEW.respuestas_blanco <> OLD.respuestas_blanco OR NEW.numero_calculo <> OLD.numero_calculo THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Para cambiar un resultado debe crearse otro calculo';
    END IF;
    IF (OLD.estado = 'PUBLICADO' AND NEW.estado <> OLD.estado)
      OR (OLD.estado = 'REVISADO' AND NEW.estado = 'CALCULADO')
      OR (OLD.estado = 'CALCULADO' AND NEW.estado = 'PUBLICADO') THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Transicion invalida de resultado';
    END IF;
    IF NEW.estado = 'REVISADO' AND OLD.estado = 'CALCULADO' THEN
        IF NEW.revisado_por IS NULL THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Se requiere responsable de revision';
        END IF;
        IF (SELECT COUNT(*) FROM detalle_resultado WHERE id_resultado = NEW.id_resultado)
            <> (SELECT COUNT(*) FROM examen_preguntas WHERE id_version_examen = NEW.id_version)
          OR NEW.respuestas_correctas <> (SELECT COUNT(*) FROM detalle_resultado WHERE id_resultado = NEW.id_resultado AND es_correcta = 1)
          OR NEW.respuestas_incorrectas <> (SELECT COUNT(*) FROM detalle_resultado WHERE id_resultado = NEW.id_resultado AND tipo_respuesta = 'UNICA' AND es_correcta = 0)
          OR NEW.respuestas_blanco <> (SELECT COUNT(*) FROM detalle_resultado WHERE id_resultado = NEW.id_resultado AND tipo_respuesta <> 'UNICA')
          OR NEW.puntaje_obtenido <> GREATEST(0, COALESCE((SELECT SUM(puntaje_obtenido) FROM detalle_resultado WHERE id_resultado = NEW.id_resultado), 0)) THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El detalle y los totales del resultado no coinciden';
        END IF;
        SET NEW.fecha_revision = NOW();
    END IF;
END$$

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

-- Primera publicación: acción del coordinador. Recalificación de un examen ya
-- publicado: la aplicación llama automáticamente a este procedimiento al finalizar
-- el lote validado; no requiere una segunda aprobación de publicación.
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

CREATE VIEW vw_historial_ranking AS
SELECT p.id_publicacion, p.id_examen, p.numero_publicacion, p.fecha_publicacion,
    p.publicada_por, r.id_estudiante, r.puntaje_obtenido, pr.posicion
FROM publicaciones_examen p
INNER JOIN publicacion_resultados pr ON pr.id_publicacion = p.id_publicacion
INNER JOIN resultados_examen r ON r.id_resultado = pr.id_resultado;

DELIMITER $$
CREATE TRIGGER trg_alternativas_pregunta_insert BEFORE INSERT ON alternativas_pregunta FOR EACH ROW
BEGIN
 IF EXISTS (SELECT 1 FROM pregunta_versiones WHERE id_version = NEW.id_version AND sellada = 1) THEN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Contenido sellado: crear nueva version de pregunta';
 END IF;
END$$
CREATE TRIGGER trg_alternativas_pregunta_update BEFORE UPDATE ON alternativas_pregunta FOR EACH ROW
BEGIN
 IF EXISTS (SELECT 1 FROM pregunta_versiones WHERE id_version = OLD.id_version AND sellada = 1) OR EXISTS (SELECT 1 FROM pregunta_versiones WHERE id_version = NEW.id_version AND sellada = 1) THEN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Contenido sellado: crear nueva version de pregunta';
 END IF;
END$$
CREATE TRIGGER trg_alternativas_pregunta_delete BEFORE DELETE ON alternativas_pregunta FOR EACH ROW
BEGIN
 IF EXISTS (SELECT 1 FROM pregunta_versiones WHERE id_version = OLD.id_version AND sellada = 1) THEN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Contenido sellado: crear nueva version de pregunta';
 END IF;
END$$
CREATE TRIGGER trg_pregunta_imagenes_insert BEFORE INSERT ON pregunta_imagenes FOR EACH ROW
BEGIN
 IF EXISTS (SELECT 1 FROM pregunta_versiones WHERE id_version = NEW.id_version AND sellada = 1) THEN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Contenido sellado: crear nueva version de pregunta';
 END IF;
END$$
CREATE TRIGGER trg_pregunta_imagenes_update BEFORE UPDATE ON pregunta_imagenes FOR EACH ROW
BEGIN
 IF EXISTS (SELECT 1 FROM pregunta_versiones WHERE id_version = OLD.id_version AND sellada = 1) OR EXISTS (SELECT 1 FROM pregunta_versiones WHERE id_version = NEW.id_version AND sellada = 1) THEN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Contenido sellado: crear nueva version de pregunta';
 END IF;
END$$
CREATE TRIGGER trg_pregunta_imagenes_delete BEFORE DELETE ON pregunta_imagenes FOR EACH ROW
BEGIN
 IF EXISTS (SELECT 1 FROM pregunta_versiones WHERE id_version = OLD.id_version AND sellada = 1) THEN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Contenido sellado: crear nueva version de pregunta';
 END IF;
END$$
CREATE TRIGGER trg_fijar_examen_ejes_insert BEFORE INSERT ON examen_ejes FOR EACH ROW
BEGIN
 IF EXISTS (SELECT 1 FROM examenes WHERE id_examen = NEW.id_examen AND estado IN ('APROBADO','APLICADO','CERRADO')) THEN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No modificar estructura confirmada ni detalle revisado';
 END IF;
END$$
CREATE TRIGGER trg_fijar_examen_ejes_update BEFORE UPDATE ON examen_ejes FOR EACH ROW
BEGIN
 IF EXISTS (SELECT 1 FROM examenes WHERE id_examen = OLD.id_examen AND estado IN ('APROBADO','APLICADO','CERRADO')) OR EXISTS (SELECT 1 FROM examenes WHERE id_examen = NEW.id_examen AND estado IN ('APROBADO','APLICADO','CERRADO')) THEN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No modificar estructura confirmada ni detalle revisado';
 END IF;
END$$
CREATE TRIGGER trg_fijar_examen_ejes_delete BEFORE DELETE ON examen_ejes FOR EACH ROW
BEGIN
 IF EXISTS (SELECT 1 FROM examenes WHERE id_examen = OLD.id_examen AND estado IN ('APROBADO','APLICADO','CERRADO')) THEN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No modificar estructura confirmada ni detalle revisado';
 END IF;
END$$
CREATE TRIGGER trg_fijar_distribucion_examen_insert BEFORE INSERT ON distribucion_examen FOR EACH ROW
BEGIN
 IF EXISTS (SELECT 1 FROM examenes WHERE id_examen = NEW.id_examen AND estado IN ('APROBADO','APLICADO','CERRADO')) THEN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No modificar estructura confirmada ni detalle revisado';
 END IF;
END$$
CREATE TRIGGER trg_fijar_distribucion_examen_update BEFORE UPDATE ON distribucion_examen FOR EACH ROW
BEGIN
 IF EXISTS (SELECT 1 FROM examenes WHERE id_examen = OLD.id_examen AND estado IN ('APROBADO','APLICADO','CERRADO')) OR EXISTS (SELECT 1 FROM examenes WHERE id_examen = NEW.id_examen AND estado IN ('APROBADO','APLICADO','CERRADO')) THEN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No modificar estructura confirmada ni detalle revisado';
 END IF;
END$$
CREATE TRIGGER trg_fijar_distribucion_examen_delete BEFORE DELETE ON distribucion_examen FOR EACH ROW
BEGIN
 IF EXISTS (SELECT 1 FROM examenes WHERE id_examen = OLD.id_examen AND estado IN ('APROBADO','APLICADO','CERRADO')) THEN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No modificar estructura confirmada ni detalle revisado';
 END IF;
END$$
CREATE TRIGGER trg_fijar_examen_preguntas_insert BEFORE INSERT ON examen_preguntas FOR EACH ROW
BEGIN
 IF EXISTS (SELECT 1 FROM versiones_examen v INNER JOIN examenes e ON e.id_examen = v.id_examen WHERE v.id_version = NEW.id_version_examen AND e.estado IN ('APROBADO','APLICADO','CERRADO')) THEN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No modificar estructura confirmada ni detalle revisado';
 END IF;
END$$
CREATE TRIGGER trg_fijar_examen_preguntas_update BEFORE UPDATE ON examen_preguntas FOR EACH ROW
BEGIN
 IF EXISTS (SELECT 1 FROM versiones_examen v INNER JOIN examenes e ON e.id_examen = v.id_examen WHERE v.id_version = OLD.id_version_examen AND e.estado IN ('APROBADO','APLICADO','CERRADO')) OR EXISTS (SELECT 1 FROM versiones_examen v INNER JOIN examenes e ON e.id_examen = v.id_examen WHERE v.id_version = NEW.id_version_examen AND e.estado IN ('APROBADO','APLICADO','CERRADO')) THEN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No modificar estructura confirmada ni detalle revisado';
 END IF;
END$$
CREATE TRIGGER trg_fijar_examen_preguntas_delete BEFORE DELETE ON examen_preguntas FOR EACH ROW
BEGIN
 IF EXISTS (SELECT 1 FROM versiones_examen v INNER JOIN examenes e ON e.id_examen = v.id_examen WHERE v.id_version = OLD.id_version_examen AND e.estado IN ('APROBADO','APLICADO','CERRADO')) THEN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No modificar estructura confirmada ni detalle revisado';
 END IF;
END$$
CREATE TRIGGER trg_fijar_versiones_examen_insert BEFORE INSERT ON versiones_examen FOR EACH ROW
BEGIN
 IF EXISTS (SELECT 1 FROM examenes WHERE id_examen = NEW.id_examen AND estado IN ('APROBADO','APLICADO','CERRADO')) THEN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No modificar estructura confirmada ni detalle revisado';
 END IF;
END$$
CREATE TRIGGER trg_fijar_versiones_examen_update BEFORE UPDATE ON versiones_examen FOR EACH ROW
BEGIN
 IF EXISTS (SELECT 1 FROM examenes WHERE id_examen = OLD.id_examen AND estado IN ('APROBADO','APLICADO','CERRADO')) OR EXISTS (SELECT 1 FROM examenes WHERE id_examen = NEW.id_examen AND estado IN ('APROBADO','APLICADO','CERRADO')) THEN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No modificar estructura confirmada ni detalle revisado';
 END IF;
END$$
CREATE TRIGGER trg_fijar_versiones_examen_delete BEFORE DELETE ON versiones_examen FOR EACH ROW
BEGIN
 IF EXISTS (SELECT 1 FROM examenes WHERE id_examen = OLD.id_examen AND estado IN ('APROBADO','APLICADO','CERRADO')) THEN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No modificar estructura confirmada ni detalle revisado';
 END IF;
END$$
CREATE TRIGGER trg_fijar_plantilla_respuestas_insert BEFORE INSERT ON plantilla_respuestas FOR EACH ROW
BEGIN
 IF EXISTS (SELECT 1 FROM revisiones_clave WHERE id_revision_clave = NEW.id_revision_clave AND estado = 'CONFIRMADA') THEN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No modificar estructura confirmada ni detalle revisado';
 END IF;
END$$
CREATE TRIGGER trg_fijar_plantilla_respuestas_update BEFORE UPDATE ON plantilla_respuestas FOR EACH ROW
BEGIN
 IF EXISTS (SELECT 1 FROM revisiones_clave WHERE id_revision_clave = OLD.id_revision_clave AND estado = 'CONFIRMADA') OR EXISTS (SELECT 1 FROM revisiones_clave WHERE id_revision_clave = NEW.id_revision_clave AND estado = 'CONFIRMADA') THEN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No modificar estructura confirmada ni detalle revisado';
 END IF;
END$$
CREATE TRIGGER trg_fijar_plantilla_respuestas_delete BEFORE DELETE ON plantilla_respuestas FOR EACH ROW
BEGIN
 IF EXISTS (SELECT 1 FROM revisiones_clave WHERE id_revision_clave = OLD.id_revision_clave AND estado = 'CONFIRMADA') THEN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No modificar estructura confirmada ni detalle revisado';
 END IF;
END$$
CREATE TRIGGER trg_fijar_detalle_resultado_insert BEFORE INSERT ON detalle_resultado FOR EACH ROW
BEGIN
 IF EXISTS (SELECT 1 FROM resultados_examen WHERE id_resultado = NEW.id_resultado AND estado IN ('REVISADO','PUBLICADO')) THEN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No modificar estructura confirmada ni detalle revisado';
 END IF;
END$$
CREATE TRIGGER trg_fijar_detalle_resultado_update BEFORE UPDATE ON detalle_resultado FOR EACH ROW
BEGIN
 IF EXISTS (SELECT 1 FROM resultados_examen WHERE id_resultado = OLD.id_resultado AND estado IN ('REVISADO','PUBLICADO')) OR EXISTS (SELECT 1 FROM resultados_examen WHERE id_resultado = NEW.id_resultado AND estado IN ('REVISADO','PUBLICADO')) THEN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No modificar estructura confirmada ni detalle revisado';
 END IF;
END$$
CREATE TRIGGER trg_fijar_detalle_resultado_delete BEFORE DELETE ON detalle_resultado FOR EACH ROW
BEGIN
 IF EXISTS (SELECT 1 FROM resultados_examen WHERE id_resultado = OLD.id_resultado AND estado IN ('REVISADO','PUBLICADO')) THEN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No modificar estructura confirmada ni detalle revisado';
 END IF;
END$$
CREATE TRIGGER trg_fijar_resultado_materia_insert BEFORE INSERT ON resultado_materia FOR EACH ROW
BEGIN
 IF EXISTS (SELECT 1 FROM resultados_examen WHERE id_resultado = NEW.id_resultado AND estado IN ('REVISADO','PUBLICADO')) THEN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No modificar estructura confirmada ni detalle revisado';
 END IF;
END$$
CREATE TRIGGER trg_fijar_resultado_materia_update BEFORE UPDATE ON resultado_materia FOR EACH ROW
BEGIN
 IF EXISTS (SELECT 1 FROM resultados_examen WHERE id_resultado = OLD.id_resultado AND estado IN ('REVISADO','PUBLICADO')) OR EXISTS (SELECT 1 FROM resultados_examen WHERE id_resultado = NEW.id_resultado AND estado IN ('REVISADO','PUBLICADO')) THEN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No modificar estructura confirmada ni detalle revisado';
 END IF;
END$$
CREATE TRIGGER trg_fijar_resultado_materia_delete BEFORE DELETE ON resultado_materia FOR EACH ROW
BEGIN
 IF EXISTS (SELECT 1 FROM resultados_examen WHERE id_resultado = OLD.id_resultado AND estado IN ('REVISADO','PUBLICADO')) THEN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No modificar estructura confirmada ni detalle revisado';
 END IF;
END$$
CREATE TRIGGER trg_configuracion_inmutable BEFORE UPDATE ON configuracion_puntaje FOR EACH ROW
BEGIN
 IF OLD.estado = 'CONFIRMADA' THEN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Crear otra revision de la politica de puntaje';
 END IF;
END$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER trg_periodo_estudiante_area_historial_insert BEFORE INSERT ON estudiante_area_historial FOR EACH ROW
BEGIN
 DECLARE v_estudiante INT;
 SELECT id_estudiante INTO v_estudiante FROM estudiantes WHERE id_estudiante = NEW.id_estudiante FOR UPDATE;
 IF EXISTS (SELECT 1 FROM estudiante_area_historial h WHERE h.id_estudiante = NEW.id_estudiante 
   AND (NEW.fecha_fin IS NULL OR h.fecha_inicio < NEW.fecha_fin)
   AND (h.fecha_fin IS NULL OR NEW.fecha_inicio < h.fecha_fin)) THEN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Los periodos del estudiante no pueden superponerse';
 END IF;
END$$
CREATE TRIGGER trg_periodo_estudiante_area_historial_update BEFORE UPDATE ON estudiante_area_historial FOR EACH ROW
BEGIN
 DECLARE v_estudiante INT;
 SELECT id_estudiante INTO v_estudiante FROM estudiantes WHERE id_estudiante = NEW.id_estudiante FOR UPDATE;
 IF EXISTS (SELECT 1 FROM estudiante_area_historial h WHERE h.id_estudiante = NEW.id_estudiante AND h.id_historial <> OLD.id_historial
   AND (NEW.fecha_fin IS NULL OR h.fecha_inicio < NEW.fecha_fin)
   AND (h.fecha_fin IS NULL OR NEW.fecha_inicio < h.fecha_fin)) THEN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Los periodos del estudiante no pueden superponerse';
 END IF;
END$$
CREATE TRIGGER trg_periodo_estudiante_grupo_historial_insert BEFORE INSERT ON estudiante_grupo_historial FOR EACH ROW
BEGIN
 DECLARE v_estudiante INT;
 SELECT id_estudiante INTO v_estudiante FROM estudiantes WHERE id_estudiante = NEW.id_estudiante FOR UPDATE;
 IF EXISTS (SELECT 1 FROM estudiante_grupo_historial h WHERE h.id_estudiante = NEW.id_estudiante 
   AND (NEW.fecha_fin IS NULL OR h.fecha_inicio < NEW.fecha_fin)
   AND (h.fecha_fin IS NULL OR NEW.fecha_inicio < h.fecha_fin)) THEN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Los periodos del estudiante no pueden superponerse';
 END IF;
END$$
CREATE TRIGGER trg_periodo_estudiante_grupo_historial_update BEFORE UPDATE ON estudiante_grupo_historial FOR EACH ROW
BEGIN
 DECLARE v_estudiante INT;
 SELECT id_estudiante INTO v_estudiante FROM estudiantes WHERE id_estudiante = NEW.id_estudiante FOR UPDATE;
 IF EXISTS (SELECT 1 FROM estudiante_grupo_historial h WHERE h.id_estudiante = NEW.id_estudiante AND h.id_historial <> OLD.id_historial
   AND (NEW.fecha_fin IS NULL OR h.fecha_inicio < NEW.fecha_fin)
   AND (h.fecha_fin IS NULL OR NEW.fecha_inicio < h.fecha_fin)) THEN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Los periodos del estudiante no pueden superponerse';
 END IF;
END$$

DELIMITER ;

-- La resolución efectiva se fija en cada detalle, incluyendo la corrección usada.
DELIMITER $$
CREATE TRIGGER trg_detalle_calificacion
BEFORE INSERT ON detalle_resultado FOR EACH ROW
BEGIN
    DECLARE v_respuesta INT;
    DECLARE v_correccion INT;
    DECLARE v_proceso INT;
    DECLARE v_clave INT;
    DECLARE v_config INT;
    DECLARE v_numero INT;
    DECLARE v_puntaje DECIMAL(24,9);
    DECLARE v_penalizacion DECIMAL(24,9);
    DECLARE v_lectura VARCHAR(5);
    DECLARE v_tipo VARCHAR(30);
    DECLARE v_correcta CHAR(1);
    DECLARE v_es_correcta BOOLEAN;
    DECLARE v_esperado DECIMAL(24,9);
    SELECT id_procesamiento,id_revision_clave,id_configuracion INTO v_proceso,v_clave,v_config
    FROM resultados_examen WHERE id_resultado=NEW.id_resultado;
    SELECT numero_pregunta,puntaje INTO v_numero,v_puntaje FROM examen_preguntas WHERE id_examen_pregunta=NEW.id_examen_pregunta;
    SELECT id_respuesta_detectada,respuesta_detectada INTO v_respuesta,v_lectura
    FROM respuestas_detectadas WHERE id_procesamiento=v_proceso AND numero_pregunta=v_numero;
    SELECT MAX(id_correccion) INTO v_correccion FROM correcciones_manual WHERE id_respuesta_detectada=v_respuesta;
    SET NEW.id_respuesta_detectada=v_respuesta;
    SET NEW.id_correccion_aplicada=v_correccion;
    IF NEW.id_correccion_aplicada IS NOT NULL THEN
        SELECT respuesta_nueva,CASE resolucion WHEN 'MARCA_UNICA' THEN 'UNICA' ELSE resolucion END
        INTO v_lectura,v_tipo FROM correcciones_manual WHERE id_correccion=NEW.id_correccion_aplicada;
    ELSE
        SET v_tipo=IF(v_lectura IS NULL, 'BLANCO', 'UNICA');
    END IF;
    SELECT respuesta_correcta INTO v_correcta FROM plantilla_respuestas WHERE id_revision_clave=v_clave AND numero_pregunta=v_numero;
    SELECT IF(usa_penalizacion,puntaje_incorrecta,0) INTO v_penalizacion FROM configuracion_puntaje WHERE id_configuracion=v_config;
    SET v_es_correcta=IF(v_tipo='UNICA' AND v_lectura=v_correcta,1,0);
    SET v_esperado=CASE WHEN v_tipo <> 'UNICA' THEN 0 WHEN v_es_correcta THEN v_puntaje ELSE v_penalizacion END;
    IF NEW.id_respuesta_detectada IS NULL OR v_correcta IS NULL
      OR NOT (NEW.respuesta_marcada <=> v_lectura) OR NEW.tipo_respuesta <> v_tipo
      OR NOT (NEW.respuesta_correcta <=> v_correcta) OR NEW.es_correcta <> v_es_correcta
      OR NEW.puntaje_obtenido <> v_esperado THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Detalle incompatible con lectura, resolucion, clave o puntaje';
    END IF;
END$$

CREATE TRIGGER trg_examen_fecha_insert BEFORE INSERT ON examenes FOR EACH ROW
BEGIN
    IF NOT (NEW.fecha_programada <=> (SELECT fecha FROM simulacros WHERE id_simulacro=NEW.id_simulacro)) OR NEW.fecha_programada IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La fecha del examen debe coincidir con la del simulacro';
    END IF;
    IF NEW.estado NOT IN ('BORRADOR','CONFIGURACION') THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Crear examen en borrador antes de validar su estructura';
    END IF;
END$$

CREATE TRIGGER trg_examen_fecha_update BEFORE UPDATE ON examenes FOR EACH ROW
BEGIN
    IF NOT (NEW.fecha_programada <=> (SELECT fecha FROM simulacros WHERE id_simulacro=NEW.id_simulacro)) OR NEW.fecha_programada IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La fecha del examen debe coincidir con la del simulacro';
    END IF;
END$$

CREATE TRIGGER trg_simulacro_fecha BEFORE UPDATE ON simulacros FOR EACH ROW
BEGIN
    IF NOT (NEW.fecha <=> OLD.fecha) AND EXISTS (SELECT 1 FROM examenes WHERE id_simulacro=OLD.id_simulacro) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No cambiar la fecha de un simulacro que ya tiene examenes';
    END IF;
END$$

CREATE TRIGGER trg_detalle_no_editar BEFORE UPDATE ON detalle_resultado FOR EACH ROW
BEGIN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No editar un detalle calculado; crear otro calculo';
END$$

CREATE PROCEDURE sp_finalizar_recalificacion(IN p_examen INT, IN p_usuario INT)
BEGIN
    -- Llamada automática del servicio al terminar la validación del lote.
    IF EXISTS (SELECT 1 FROM publicaciones_examen WHERE id_examen=p_examen) THEN
        CALL sp_publicar_examen(p_examen,p_usuario);
    END IF;
END$$

CREATE TRIGGER trg_registrar_aprobacion_inicial
AFTER UPDATE ON preguntas FOR EACH ROW
BEGIN
    IF NEW.estado = 'APROBADA' AND OLD.estado <> 'APROBADA' THEN
        INSERT INTO revisiones_pregunta(id_version_pregunta,id_pregunta,id_usuario_revision,
            estado_anterior,estado_nuevo,observacion)
        SELECT id_version,NEW.id_pregunta,NEW.aprobado_por,OLD.estado,NEW.estado,'Aprobacion inicial'
        FROM pregunta_versiones WHERE id_pregunta=NEW.id_pregunta AND estado='ACTIVA' AND sellada=1;
    END IF;
END$$
DELIMITER ;

-- Entradas de carga OMR; las lecturas se conservan antes de registrar cartillas.
CREATE TABLE IF NOT EXISTS cargas_omr (
 id BIGINT AUTO_INCREMENT PRIMARY KEY,
 examen_id INT NOT NULL,
 usuario_id INT NOT NULL,
 operacion_id CHAR(36) NOT NULL,
 nombre_archivo VARCHAR(255) NOT NULL,
 pagina INT NOT NULL,
 huella CHAR(64) NOT NULL,
 ruta_imagen VARCHAR(255) NOT NULL,
 ruta_original VARCHAR(255) NOT NULL,
 estado ENUM('PENDIENTE','REVISAR','ERROR','DESCARTADA','REGISTRADA') NOT NULL DEFAULT 'PENDIENTE',
 lectura_json JSON NULL,
 error_texto TEXT NULL,
 motivo_descarte TEXT NULL,
 estudiante_id INT NULL,
 version_id INT NULL,
 cartilla_id INT NULL,
 creada_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 UNIQUE KEY uq_carga_operacion_pagina (operacion_id, nombre_archivo, pagina),
 FOREIGN KEY (examen_id) REFERENCES examenes(id_examen),
 FOREIGN KEY (usuario_id) REFERENCES usuarios(id_usuario),
 FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id_estudiante),
 FOREIGN KEY (cartilla_id) REFERENCES cartillas(id_cartilla),
 FOREIGN KEY (version_id, examen_id) REFERENCES versiones_examen(id_version, id_examen)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS historial_cargas_omr (
 id BIGINT AUTO_INCREMENT PRIMARY KEY,
 carga_id BIGINT NOT NULL,
 accion ENUM('REINTENTO','REEMPLAZO') NOT NULL,
 usuario_id INT NOT NULL,
 motivo TEXT NOT NULL,
 datos_anteriores JSON NOT NULL,
 creada_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY(carga_id) REFERENCES cargas_omr(id),
 FOREIGN KEY(usuario_id) REFERENCES usuarios(id_usuario),
 INDEX idx_historial_carga(carga_id,id)
) ENGINE=InnoDB;

# Inicio de implementación del sistema académico

Este documento organiza el primer trabajo a partir de `3_requisitos v2.md`, `5_flujos_y_validacion.md`, `PROTOTIPO_COMPLETO.html` y `nueva_base_de_datos.sql`, ubicados en la carpeta padre. El proyecto Flet anterior es una referencia visual y funcional; este sistema se implementa desde cero. La base contendrá datos de prueba durante el desarrollo.

## Pantallas y acciones por rol

| Perfil | Pantalla | Acciones y datos principales | Referencia |
| --- | --- | --- | --- |
| Común | Inicio de sesión | Usuario, contraseña, errores de acceso y entrada según los roles autorizados. Recuperación de acceso pendiente de concretar. | Prototipo 01; HF.1.1 y HF.1.7 |
| Coordinador | Panel | Preguntas, lecturas, cálculos y publicaciones pendientes; acceso a cada tarea. | Prototipo 02; HF.6.5 |
| Coordinador | Gestión de estudiantes | Buscar, registrar, editar, activar o desactivar; vincular una cuenta opcional sin perder historial. | Prototipo 03; HF.1.4 |
| Coordinador | Usuarios | Administrar cuentas y roles salvo DIRECTOR; no modificar cuentas con rol DIRECTOR. | Prototipo 04; HF.1.2–1.3 |
| Coordinador | Organización académica | Administrar ciclos, grupos, áreas, ejes y materias; asignar materias a docentes. | Prototipo 05; HF.1.5 |
| Coordinador | Cambios de grupo y área | Consultar asignación y cambiarla conservando periodos e historial. | Prototipo 06; HF.1.6 y HF.1.8 |
| Coordinador | Simulacros | Crear y consultar simulacros y sus exámenes. | Prototipo 07; HF.3.1.5 |
| Coordinador | Banco de preguntas | Filtrar, revisar, aprobar o devolver con observación. | Prototipo 08; HF.2.2 |
| Coordinador | Configurar examen | Seleccionar preguntas aprobadas, distribuir por materia y eje, configurar puntajes y versiones. | Prototipo 09; HF.3.1 |
| Coordinador | Clave de respuestas | Revisar, importar, corregir y confirmar una clave identificada por versión. | Prototipo 10; HF.3.2 |
| Coordinador | Procesar cartillas | Recibir archivos, identificar estudiante y versión, procesar y resolver cargas pendientes. | Prototipo 11; HF.4.1.1–1.2 y HF.4.1.4 |
| Coordinador | Revisión de lecturas | Resolver lecturas dudosas y marcas múltiples; conservar correcciones. | Prototipo 12; HF.4.1.3 |
| Coordinador | Ranking y reportes | Consultar resultados y ranking por examen y área; publicar después de revisar. | Prototipo 13; HF.4.2 y HF.6.1 |
| Coordinador | Estadísticas y reportes | Consultar indicadores y descargar reportes. | Prototipos 14–15; HF.6.4 |
| Estudiante | Mi resultado | Ver resultados publicados y desglose por materia. | Prototipo 16; HF.5.1.1 y HF.5.1.3 |
| Estudiante | Detalle por pregunta | Comparar respuesta marcada, correcta y resultado. | Prototipo 17; HF.5.1.2 |
| Estudiante | Ranking | Consultar su posición en el examen publicado. | Prototipo 18; HF.5.2.1 |
| Estudiante | Mi evolución | Ver resultados por examen a lo largo del tiempo. | Prototipo 19; HF.5.2.2 |
| Docente | Mis preguntas | Filtrar preguntas propias y consultar estado y observaciones. | Prototipo 20; HF.2.1.2 |
| Docente | Crear y editar pregunta | Registrar área, materia, tema, enunciado, alternativas y respuesta; conservar versiones, imágenes y fórmulas. | Prototipos 21–22; HF.2.1.1 y HF.2.1.3–1.5 |
| Docente | Estadísticas de materias | Consultar desempeño de preguntas de sus materias. | Prototipo 23; HF.6.2 |
| Director | Panel | Consultar indicadores institucionales y promedios. | Prototipo 24; HF.6.3 |
| Director | Administración | Administrar todos los usuarios y roles y ejecutar las funciones del coordinador. | HF.1.2–1.3; decisión de roles |
| Director | Comparativo por examen y área | Filtrar y comparar resultados entre exámenes y áreas. | Prototipo 25; HF.6.3 |
| Director | Reportes | Consultar y descargar reportes institucionales. | Prototipo 26; HF.6.4 |

Las vistas actuales en `presentacion/vistas` son HTML estático con datos de ejemplo. Los botones y enlaces no representan todavía casos de uso terminados. El formulario común dirige actualmente a un panel de demostración: la autenticación y la selección del destino deben implementarse en Flask.

## Primer recorrido de implementación

1. Preparar una instalación de MySQL de desarrollo y confirmar su versión. Crear una base de prueba aislada mediante el script revisado; no ejecutar reinicios sobre bases existentes.
2. Configurar Flask, SQLAlchemy y una conexión por variables de entorno, sin incluir credenciales reales en el repositorio. La presentación llamará a servicios de aplicación; los repositorios y la sesión estarán en infraestructura.
3. Implementar autenticación y sesión para cuentas activas con contraseña verificada. La autorización se comprueba en el servidor. Un estudiante solo puede tener rol estudiante; una cuenta no estudiante puede tener más de un rol. Definir la selección de rol cuando haya varios roles autorizados.
4. Implementar registro, búsqueda, edición y desactivación de estudiantes por un coordinador autenticado. Un estudiante puede existir sin cuenta; el código es único. La vinculación de cuenta y los cambios de asignación deben conservar el historial.
5. Conectar las vistas de acceso y gestión de estudiantes con rutas, servicios y repositorios. Mostrar mensajes y datos provenientes del servidor, incluyendo estados vacíos y errores de validación.
6. Comprobar el recorrido con datos ficticios: acceso válido e inválido, restricciones por rol, estudiante con y sin cuenta, código duplicado y conservación del historial de asignación. Después avanzar a organización académica y preguntas.

## Revisión inicial de tablas

| Necesidad | Tablas actuales | Evaluación inicial |
| --- | --- | --- |
| Cuenta y roles | `usuarios`, `roles`, `usuario_roles` | Contienen identificador, hash, estado y relaciones de roles. El SQL crea un coordinador inicial inactivo; hay que establecer un hash válido durante la preparación del entorno. |
| Permisos y destino | `permisos`, `rol_permisos`, `paneles`, `rol_paneles` | Permiten asociar permisos y paneles. Revisar si almacenar rutas en la base aporta valor una vez definidas las rutas Flask. |
| Estudiante | `estudiantes` | La cuenta es opcional y única; código único; nombres y apellidos obligatorios. `dni` no es único actualmente: confirmar si se exige unicidad antes de cambiarlo. |
| Área y grupo | `areas`, `ciclos_preparacion`, `grupos_academicos`, `estudiante_area_historial`, `estudiante_grupo_historial` | Conservan asignaciones con fechas y una asignación abierta por tipo. Los cambios deben realizarse en una transacción y respetar el convenio de fechas de los requisitos. |

### Aspectos por resolver antes de dar el esquema por definitivo

- `usuarios` y `estudiantes` guardan nombres y datos de contacto por separado. Definir cuál es la fuente de verdad al vincular una cuenta y cómo se actualiza cada dato.
- Precisar las reglas de DNI, correo, teléfono, código y campos obligatorios, así como si se permite reutilizar identificadores tras una desactivación.
- El disparador `trg_estudiante_un_solo_rol` controla inserciones en `usuario_roles`; revisar también las actualizaciones y la vinculación entre `estudiantes` y cuentas para garantizar la regla completa.
- Revisar concurrencia de los cambios de asignación y verificar las restricciones y disparadores contra la versión concreta de MySQL seleccionada.
- El archivo menciona `7_correcciones_y_criterios.md`, que no aparece en los archivos revisados. Las decisiones necesarias se documentarán con las fuentes disponibles y se confirmarán cuando corresponda.
- No se ha ejecutado el script SQL durante esta revisión. Antes de considerarlo instalable hay que crear una base aislada y verificar tablas, vistas, disparadores, procedimientos y datos iniciales.

## Referencias visuales

El login, la cabecera, el menú lateral, las tarjetas y la paleta se tomarán de `SISTEMA_ACADEMICO_2026/src/login.py`, `src/componentes` y `src/assets`. `PROTOTIPO_COMPLETO.html` describe contenidos y recorridos por rol. La presentación final se implementará con HTML/CSS y se integrará a Flask sin trasladar las dependencias Flet al proyecto nuevo.

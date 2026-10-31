# Práctica 8 – Prototipo Inicial

**Parte 1:** mapeo de las features BDD a los puntos de contacto (touchpoints) de los mapas de experiencia de las personas priorizadas.

**Proyecto:** Sistema de Gestión de Exámenes y Rendimiento Académico

**Personas priorizadas:** Patricia Salazar (coordinadora, persona principal), Pedro Gómez (estudiante), Juan (docente) y Ricardo Medina (director).

**Leyenda de emoción:** ● marca la emoción dominante de cada etapa.

---

## Mapa de experiencia 1 – Patricia Salazar (Coordinadora académica)

| | |
|---|---|
| **Contexto** | Antes y después de un simulacro, Patricia debe preparar el examen, recibir las cartillas, calificarlas y publicar los resultados a tiempo para los estudiantes y la dirección. |
| **Objetivo** | Calificar el examen y publicar los resultados de forma rápida y sin errores. |

| | | Etapa 1: Preparar el examen | Etapa 2: Registrar las cartillas | Etapa 3: Revisar las lecturas | Etapa 4: Publicar y analizar |
|---|---|---|---|---|---|
| **Acciones** | | Revisa y aprueba las preguntas de los docentes. Arma el examen por área, con pesos por eje y versiones A/B que reordenan las mismas preguntas. | Carga la imagen de cada cartilla (escaneada o fotografiada), la asocia al estudiante y al examen, y deja que el sistema lea las respuestas. | Revisa las lecturas con confianza menor a 80% o con más de una marca y corrige las que sean necesarias. | Revisa el puntaje calculado y publica el examen; una recalificación posterior actualiza automáticamente el puntaje y ranking al finalizar y consulta el ranking y las estadísticas. |
| **Emoción** | Positiva | ● | | | ● |
| | Neutral | | ● | | |
| | Negativa | | | ● | |
| **Punto de contacto o canal** | | Aplicación web: pantallas *Banco de preguntas* y *Configurar examen* | Aplicación web: pantalla *Procesar cartillas* | Aplicación web: pantalla *Revisión de lecturas* | Aplicación web: pantallas *Resultados*, *Ranking* y *Reportes* |
| **Feature BDD** | | **Aprobar preguntas del banco** (RF.2)<br>**Crear simulacro** (RF.3)<br>**Configurar examen por área** (RF.3)<br>**Revisar clave de respuestas** (RF.3) | **Registrar cartilla** y **Leer respuestas** (RF.4) | **Corregir lecturas dudosas** (RF.4) | **Calcular y publicar resultados** (RF.4)<br>**Consultar ranking y reportes** (RF.6) |



## Mapa de experiencia 2 – Pedro Gómez (Estudiante)

| | |
|---|---|
| **Contexto** | Después de rendir un simulacro, Pedro quiere saber cuánto sacó, en qué se equivocó y cómo va frente a sus compañeros, usando su celular. |
| **Objetivo** | Conocer sus resultados y sus errores para mejorar en el siguiente examen. |

| | | Etapa 1: Ingresar al sistema | Etapa 2: Ver su resultado | Etapa 3: Analizar sus errores | Etapa 4: Compararse y planificar |
|---|---|---|---|---|---|
| **Acciones** | | Abre el sistema desde su celular e inicia sesión. | Consulta su puntaje y su posición apenas se publican los resultados. | Revisa por pregunta qué marcó y cuál era la correcta, y el desglose por materia. | Compara su posición en el ranking y revisa su evolución entre simulacros. |
| **Emoción** | Positiva | | ● | | ● |
| | Neutral | ● | | | |
| | Negativa | | | ● | |
| **Punto de contacto o canal** | | Celular: aplicación web, pantalla *Inicio de sesión* | Celular: pantalla *Mi resultado* | Celular: pantallas *Detalle por pregunta* y *Desglose por materia* | Celular: pantallas *Ranking* y *Mi evolución* |
| **Feature BDD** | | **Iniciar sesión** (RF.1) | **Consultar resultados publicados** (RF.5) | **Ver detalle de errores por pregunta y materia** (RF.5) | **Ver ranking y evolución** (RF.5) |



## Mapa de experiencia 3 – Juan (Docente)

| | |
|---|---|
| **Contexto** | Antes de cada simulacro, Juan elabora preguntas de Matemática, las envía al coordinador y después quiere saber cómo respondieron los estudiantes. |
| **Objetivo** | Aportar preguntas de calidad y mejorar a partir del desempeño de los estudiantes. |

| | | Etapa 1: Crear preguntas | Etapa 2: Enviar y dar seguimiento | Etapa 3: Corregir según observaciones | Etapa 4: Revisar el desempeño |
|---|---|---|---|---|---|
| **Acciones** | | Registra cada pregunta con su(s) área(s), eje temático, materia, tema, enunciado, alternativas (con imagen o fórmulas si las necesita) y respuesta correcta. | Envía las preguntas a revisión y consulta su estado (borrador, revisión, aprobada). | Si el coordinador devuelve una pregunta, lee la observación y la edita, generando una nueva versión. | Consulta cómo respondieron los estudiantes a sus preguntas y materias. |
| **Emoción** | Positiva | | ● | | ● |
| | Neutral | ● | | | |
| | Negativa | | | ● | |
| **Punto de contacto o canal** | | Aplicación web: pantalla *Crear pregunta* | Aplicación web: pantalla *Mis preguntas* | Aplicación web: pantalla *Editar pregunta* | Aplicación web: pantalla *Estadísticas de mis materias* |
| **Feature BDD** | | **Crear y editar preguntas** (RF.2) | **Consultar estado de mis preguntas** (RF.2) | **Editar pregunta conservando versiones** (RF.2) | **Ver estadísticas de mis materias** (RF.6) |



## Mapa de experiencia 4 – Ricardo Medina (Director)

| | |
|---|---|
| **Contexto** | Al cerrar un ciclo de simulacros, Ricardo revisa cómo va la academia para decidir acciones de mejora. |
| **Objetivo** | Contar con información institucional oportuna para tomar decisiones estratégicas. |

| | | Etapa 1: Ingresar al sistema | Etapa 2: Ver indicadores generales | Etapa 3: Comparar exámenes y áreas | Etapa 4: Descargar y compartir reportes |
|---|---|---|---|---|---|
| **Acciones** | | Inicia sesión con su usuario. | Revisa promedios, puntajes y cantidad de estudiantes evaluados. | Compara el rendimiento entre exámenes y entre áreas para ver la evolución. | Descarga reportes en PDF o Excel para presentarlos. |
| **Emoción** | Positiva | | ● | | ● |
| | Neutral | ● | | ● | |
| | Negativa | | | | |
| **Punto de contacto o canal** | | Aplicación web: pantalla *Inicio de sesión* | Aplicación web: pantalla *Panel del director* | Aplicación web: pantalla *Comparativo por examen y área* | Aplicación web: pantalla *Reportes* |
| **Feature BDD** | | **Iniciar sesión** (RF.1) | **Consultar estadísticas institucionales** (RF.6) | **Comparar rendimiento entre exámenes y áreas** (RF.6) | **Descargar reportes** (RF.6) |



## Resumen: feature BDD ↔ pantalla del prototipo

| Feature BDD | Requisito | Pantalla a diseñar | Persona |
|---|---|---|---|
| Iniciar sesión | RF.1 | Inicio de sesión | Todas |
| Gestionar usuarios y roles | RF.1 | Gestión de usuarios | Patricia |
| Gestionar estudiantes | RF.1 | Gestión de estudiantes | Patricia |
| Crear simulacro | RF.3 | Simulacros | Patricia |
| Ver pendientes del coordinador | RF.6 | Panel del coordinador | Patricia |
| Consultar estadísticas por categoría | RF.6 | Estadísticas | Patricia |
| Aprobar preguntas del banco | RF.2 | Banco de preguntas | Patricia |
| Configurar examen por área | RF.3 | Configurar examen | Patricia |
| Revisar clave de respuestas | RF.3 | Revisión de clave | Patricia |
| Registrar cartilla y leer respuestas | RF.4 | Procesar cartillas | Patricia |
| Corregir lecturas dudosas | RF.4 | Revisión de lecturas | Patricia |
| Calcular y publicar resultados | RF.4 | Resultados (vista del coordinador) | Patricia |
| Consultar ranking y reportes | RF.6 | Ranking y reportes | Patricia |
| Consultar resultados publicados | RF.5 | Mi resultado | Pedro |
| Ver detalle de errores por pregunta y materia | RF.5 | Detalle por pregunta y desglose por materia | Pedro |
| Ver ranking y evolución | RF.5 | Ranking y mi evolución | Pedro |
| Editar pregunta conservando versiones | RF.2 | Editar pregunta | Juan |
| Crear y editar preguntas | RF.2 | Crear pregunta | Juan |
| Consultar estado de mis preguntas | RF.2 | Mis preguntas | Juan |
| Ver estadísticas de mis materias | RF.6 | Estadísticas de mis materias | Juan |
| Consultar estadísticas institucionales | RF.6 | Panel del director | Ricardo |
| Comparar rendimiento entre exámenes y áreas | RF.6 | Comparativo por examen y área | Ricardo |
| Descargar reportes | RF.6 | Reportes | Ricardo |

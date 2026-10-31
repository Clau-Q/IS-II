**Proyecto:** Sistema de Gestión de Exámenes y Rendimiento Académico


## 1) Contexto social

**Sector:** Educación (academias preuniversitarias).

Las academias preuniversitarias preparan a estudiantes para los exámenes de admisión universitaria. Para ello aplican simulacros y exámenes periódicos, cuyos resultados son la principal fuente para saber si el estudiante mejora y en qué cursos falla.

En muchas academias, la calificación de estos exámenes y el seguimiento de resultados se hacen de forma manual o con herramientas no integradas (hojas de cálculo, archivos sueltos). Esto genera:

- **Retrasos** en la entrega de resultados: el estudiante los recibe cuando ya pasó el momento útil para corregir sus errores.
- **Errores en la calificación** por el trabajo manual y repetitivo.
- **Datos dispersos y duplicados:** preguntas, notas y rankings en archivos distintos.
- **Dificultad para hacer seguimiento** del progreso del estudiante por curso y a lo largo del ciclo.
- **Estrés en los alumnos** por la falta de retroalimentación rápida.
- **Decisiones tardías** de coordinación y dirección por falta de estadísticas oportunas.

> Pendiente de validar con entrevistas: tiempo actual de calificación por examen, cantidad de estudiantes por examen y frecuencia de los simulacros.

---

## 2) Función o proceso de negocio

| Función / Proceso | Descripción | Producto |
|---|---|---|
| Calificación y seguimiento académico | Automatización de la calificación de exámenes, generación de rankings y visualización del progreso académico. Incluye la gestión del banco de preguntas desde el que se arman los exámenes. | Sistema de Gestión de Exámenes y Rendimiento Académico |

**Proceso actual:** el docente envía preguntas al coordinador sin un flujo ordenado → el coordinador arma el examen → se aplica el examen → se califica manualmente → las notas se pasan a una hoja de cálculo → el ranking se arma a mano → los resultados llegan tarde y sin detalle de errores.

**Proceso que el sistema mejora:** gestión de preguntas con aprobación → armado del examen → calificación → publicación de resultados → ranking y seguimiento del progreso.

---

## 3) Stakeholders

| Stakeholder | Directo / Afectado | Descripción |
|---|---|---|
| Estudiantes | Directo | Obtienen resultados rápidos, conocen su posición en el ranking, identifican sus errores y mejoran su rendimiento. |
| Docentes | Directo | Registran preguntas para los exámenes, revisan resultados y analizan el desempeño en sus materias. |
| Coordinadores académicos | Directo | Aprueban preguntas, arman exámenes, supervisan rankings, estadísticas y el rendimiento general de la academia. |
| Director | Directo | Supervisa el funcionamiento de la institución a partir de reportes y estadísticas. |
| Padres de familia | Afectado | Revisan el rendimiento de sus hijos y toman decisiones educativas. No usan el sistema directamente. |

---

## 4) Objetivos externos de los stakeholders

| Stakeholder | Objetivos externos |
|---|---|
| Estudiantes | Superarse en la vida y acceder a una educación universitaria. |
| Docentes | Lograr que sus estudiantes comprendan los temas y mejorar la calidad del aprendizaje. |
| Coordinadores académicos | Supervisar el rendimiento general de los estudiantes mediante estadísticas y rankings, y mejorar su desempeño. |
| Padres de familia | Acceder a información clara y oportuna sobre el rendimiento académico de sus hijos para apoyar su proceso educativo y tomar decisiones. |
| Director | Mejorar la calidad educativa de la institución y fortalecer su prestigio académico. |

---

## 5) Fuentes de información

| Fuente | Descripción | URL |
|---|---|---|
| Stakeholders (estudiantes preuniversitarios) | Señalan dificultades en el seguimiento académico, control de notas y acceso a información oportuna para la toma de decisiones. | — |
| Stakeholders (coordinadores) | Evidencian problemas en el manejo de información (notas, evaluaciones). | — |
| Tesis UCV (Ramírez) | Evidencia que la gestión académica basada en procesos manuales o herramientas no integradas genera duplicidad de datos, errores en el registro de notas y deficiente acceso a la información, afectando la toma de decisiones. | https://repositorio.ucv.edu.pe/bitstream/handle/20.500.12692/21952/Ram%c3%adrez_QC.pdf?sequence=1&isAllowed=y |
| Tesis UNC (2013) | Propone un sistema de información para mejorar la gestión académica: automatización de procesos, reducción de errores y mejor acceso a reportes. | https://repositorio.unc.edu.pe/bitstream/handle/20.500.14074/536/T%20620.7%20L392%202013.pdf?sequence=1&isAllowed=y |
| Reglas de negocio del equipo (borrador) | Definen los roles, el banco de preguntas, la configuración de exámenes, los resultados, el ranking y el seguimiento académico que el sistema debe cubrir. | — |

---

## 6) Personas

Las personas se construyeron con base en las fuentes del punto 5: la información de estudiantes y coordinadores, las tesis revisadas y las reglas de negocio del equipo.

### Número de personas y enfoque

Se definieron **5 personas** de usuarios directos: 1 coordinadora, 1 docente, 2 estudiantes y 1 director. **La persona principal es Patricia Salazar (coordinadora académica)**: es quien ejecuta el proceso que el sistema automatiza (banco de preguntas, armado de exámenes, calificación y reportes). Si el sistema funciona para ella, produce los resultados que consumen los demás.

### Cualidades y diferencias entre los usuarios

| Persona | Rol | Relación con el sistema | Nivel tecnológico | Qué necesita principalmente | Prioridad |
|---|---|---|---|---|---|
| Patricia Salazar | Coordinadora académica | Opera el proceso y genera los resultados | Básico–intermedio (Excel y Word) | Calificar rápido y sin errores, y obtener reportes confiables | **Principal** |
| Juan | Docente | Aporta contenido (preguntas) | Intermedio | Un flujo ordenado para enviar preguntas y que sean aprobadas | Secundaria |
| Pedro Gómez | Estudiante | Consume resultados | Básico–intermedio (celular y aplicaciones) | Saber en qué se equivocó y compararse con otros | Secundaria |
| Ana López | Estudiante | Consume resultados | Intermedio–alto | Análisis detallado por materia para planificar su estudio | Secundaria |
| Ricardo Medina | Director | Consume estadísticas y reportes institucionales | Intermedio | Información oportuna y agregada para tomar decisiones | Secundaria |

**Cualidades en común:** todos sufren las consecuencias del proceso manual (demoras, errores, información dispersa) y todos necesitan información clara y oportuna.

**Diferencias:**
- **Productores y consumidores de información:** Patricia y Juan generan datos; Pedro y Ana los consultan.
- **Nivel tecnológico:** de básico (Pedro, Patricia) a intermedio–alto (Ana), por lo que la interfaz debe ser simple para el menor nivel.
- **Profundidad de información:** Pedro busca saber su posición y sus errores; Ana necesita análisis por materia; Patricia necesita estadísticas generales; Ricardo necesita indicadores institucionales para decidir.

### Persona principal: Patricia Salazar

| | |
|---|---|
| **Foto/Avatar** | *(insertar foto)* |
| **Perfil** | Coordinadora académica |
| **Nombre** | Patricia Salazar |
| **Edad** | 29 |
| **Género** | Femenino |
| **Ocupación** | Coordinadora académica |
| **Educación** | Gestión Educativa |
| **Tecnología** | Microsoft Excel y Word |
| **Frase** | “Necesito una forma más rápida y segura de corregir exámenes sin cometer errores.” |
| **Objetivos** | • Optimizar el proceso de corrección de exámenes y generación de resultados (notas y rankings).<br>• Mejorar el seguimiento del rendimiento académico mediante información rápida y confiable. |
| **Tareas contextuales** | • Gestionar el banco de preguntas y elaborar exámenes a partir de ellas.<br>• Revisar evaluaciones, calcular puntajes y generar reportes de rendimiento. |
| **Motivaciones** | • Reducir el tiempo de trabajo.<br>• Contar con resultados confiables. |
| **Frustraciones** | • Proceso manual, lento y propenso a errores. |

### Persona secundaria: Juan

| | |
|---|---|
| **Foto/Avatar** | *(insertar foto)* |
| **Perfil** | Docente preuniversitario |
| **Nombre** | Juan |
| **Edad** | 34 |
| **Género** | Masculino |
| **Ocupación** | Profesor de Matemática |
| **Educación** | Licenciatura en Educación (especialidad Matemática) |
| **Tecnología** | Intermedio (maneja plataformas básicas y herramientas digitales) |
| **Frase** | “Quiero asegurarme de que mis preguntas realmente ayuden a los estudiantes a mejorar.” |
| **Objetivos** | • Aportar preguntas de calidad.<br>• Mejorar el nivel académico de los estudiantes.<br>• Contribuir al éxito de los alumnos en su ingreso a la universidad. |
| **Tareas contextuales** | • Elaborar preguntas de matemática para simulacros.<br>• Enviar preguntas al coordinador académico. |
| **Motivaciones** | • Contribuir al aprendizaje y progreso de sus estudiantes.<br>• Mantener estabilidad laboral y reconocimiento profesional. |
| **Frustraciones** | • Falta de organización en el envío de preguntas. |

### Persona secundaria: Pedro Gómez

| | |
|---|---|
| **Foto/Avatar** | *(insertar foto)* |
| **Perfil** | Estudiante preuniversitario |
| **Nombre** | Pedro Gómez |
| **Edad** | 18 |
| **Género** | Masculino |
| **Ocupación** | Estudiante preuniversitario |
| **Educación** | Secundaria completa; se prepara para el examen de admisión |
| **Tecnología** | Básico–intermedio (uso frecuente de celular y aplicaciones); consume videos educativos |
| **Frase** | “Quiero saber en qué me equivoqué para mejorar en el siguiente examen.” |
| **Objetivos** | • Ingresar a la universidad.<br>• Mejorar su rendimiento académico. |
| **Tareas contextuales** | • Revisar resultados obtenidos.<br>• Identificar las materias en las que tiene dificultades.<br>• Comparar su rendimiento con otros estudiantes (ranking). |
| **Motivaciones** | • Superarse académicamente.<br>• Alcanzar una vacante en una universidad. |
| **Frustraciones** | • Retraso en la entrega de resultados.<br>• No ver mejoras constantes en sus resultados. |

### Persona secundaria: Ana López

| | |
|---|---|
| **Foto/Avatar** | *(insertar foto)* |
| **Perfil** | Estudiante preuniversitaria |
| **Nombre** | Ana López |
| **Edad** | 17 |
| **Género** | Femenino |
| **Ocupación** | Estudiante preuniversitaria |
| **Educación** | Secundaria completa (recién egresada) |
| **Tecnología** | Intermedio–alto (usa apps educativas y plataformas online) |
| **Frase** | “Si sé exactamente en qué fallo, puedo mejorar más rápido que los demás.” |
| **Objetivos** | • Obtener un alto puntaje en los simulacros.<br>• Ingresar a una universidad de prestigio. |
| **Tareas contextuales** | • Revisar detalladamente sus resultados.<br>• Planificar su estudio según sus debilidades. |
| **Motivaciones** | • Alcanzar una carrera competitiva (medicina, ingeniería, etc.).<br>• Aprovechar al máximo su tiempo de estudio. |
| **Frustraciones** | • No contar a tiempo con el detalle de sus errores, lo que le impide planificar su estudio. |

### Persona secundaria: Ricardo Medina

| | |
|---|---|
| **Foto/Avatar** | *(insertar foto)* |
| **Perfil** | Director de academia preuniversitaria |
| **Nombre** | Ricardo Medina |
| **Edad** | 45 |
| **Género** | Masculino |
| **Ocupación** | Director de academia preuniversitaria |
| **Educación** | Licenciado en Educación con estudios en Gestión Educativa |
| **Tecnología** | Intermedio (usa correo, hojas de cálculo y reportes digitales) |
| **Frase** | “Necesito datos claros y a tiempo para decidir cómo mejorar los resultados de la academia.” |
| **Objetivos** | • Mejorar la calidad educativa de la institución.<br>• Fortalecer el prestigio académico de la academia. |
| **Tareas contextuales** | • Revisar reportes y estadísticas institucionales.<br>• Supervisar el rendimiento general por área.<br>• Evaluar la evolución de los resultados entre simulacros. |
| **Motivaciones** | • Que más estudiantes ingresen a la universidad.<br>• Que la academia sea reconocida por sus resultados. |
| **Frustraciones** | • Información tardía e incompleta para tomar decisiones estratégicas.<br>• Reportes armados manualmente que no se pueden comparar entre exámenes. |

**Prompt usado:**

```
Actúa como experto en UX.
Crea una persona (perfil de usuario) de un docente, estudiante, coordinador académico o director que trabaja en una academia preuniversitaria donde la calificación de exámenes es manual.
Incluye: nombre, edad, género, ocupación, educación, uso de tecnología, objetivos, tareas, frase, motivaciones y frustraciones.
El perfil debe reflejar problemas como retrasos, errores al calificar y carga de trabajo.
```

---

## 7) Síntesis del problema

### Problema por stakeholder

| Stakeholder | Objetivos externos | Problema (necesidad) |
|---|---|---|
| Estudiantes | Mejorar su rendimiento académico e ingresar a la universidad elegida | No reciben retroalimentación rápida ni clara sobre sus resultados, lo que dificulta identificar errores y mejorar en sus cursos. |
| Coordinadores académicos | Mejorar la calidad del aprendizaje y el seguimiento del progreso | La calificación manual consume demasiado tiempo y puede generar errores. |
| Director | Mejorar la calidad educativa y el prestigio institucional | Falta de información oportuna y precisa para tomar decisiones estratégicas que ayuden a los estudiantes a mejorar. |

### Objetivo de diseño

Diseñar un sistema de gestión de exámenes para ayudar a los estudiantes, coordinadores y director a mejorar el rendimiento académico y optimizar el proceso de evaluación.

### Problema de diseño (plantilla Design Science)

| | |
|---|---|
| **Mejorar** | El proceso de calificación manual de exámenes en academias preuniversitarias |
| **mediante** | El diseño de un sistema de gestión de exámenes y rendimiento académico |
| **que satisfaga** | Los requisitos de eficiencia, precisión y rapidez en la retroalimentación |
| **para** | Mejorar el rendimiento académico y la satisfacción estudiantil |

### Producto (plantilla UX Perspective)

| | |
|---|---|
| **Este producto es para** | Estudiantes, docentes, coordinadores académicos y director |
| **les ayudará a resolver o mejorar** | Los retrasos en la entrega de resultados, los errores en la calificación, el seguimiento del progreso del estudiante y la demora de retroalimentación |
| **mediante** | El rediseño de un artefacto |
| **para** | Automatizar el proceso de calificación y seguimiento académico, facilitando la generación de rankings y la visualización del progreso académico |

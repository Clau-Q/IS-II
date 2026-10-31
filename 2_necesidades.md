# 2 – Necesidades de los Usuarios

**Proyecto:** Sistema de Gestión de Exámenes y Rendimiento Académico


## 1. Historias Point of View (POV)

Formato: **El (usuario) necesita (necesidad) porque (propósito / insight)**. Las historias se derivan de las personas definidas en la Práctica 1.

| Historia | Usuario | Necesidad | Propósito / Insight |
|---|---|---|---|
| H.1 | Patricia (coordinadora) | Calificar los exámenes de forma rápida y sin errores | La calificación manual consume mucho tiempo y un error en una nota afecta la confianza de los estudiantes |
| H.2 | Patricia (coordinadora) | Obtener notas y rankings generados automáticamente | Hoy los arma a mano en Excel y los resultados llegan tarde |
| H.3 | Patricia (coordinadora) | Tener un banco de preguntas organizado por materia y configurar exámenes con sus versiones y estructura | Las preguntas llegan dispersas y cada examen debe tener pesos y puntajes consistentes (los pesos suman 100% y los puntajes suman el total); armarlos a mano toma mucho tiempo |
| H.4 | Patricia (coordinadora) | Revisar y aprobar las preguntas de los docentes sin perder las versiones anteriores | Debe garantizar la calidad de las preguntas y poder saber qué se usó en cada examen |
| H.5 | Patricia (coordinadora) | Generar reportes de rendimiento por examen, área y materia | Debe supervisar el rendimiento general y mostrar resultados a la dirección |
| H.6 | Juan (docente) | Enviar sus preguntas de forma ordenada al coordinador | Hoy el envío es desorganizado y no sabe si sus preguntas fueron revisadas o usadas |
| H.7 | Juan (docente) | Saber cómo respondieron los estudiantes a sus preguntas y materias | Quiere mejorar la calidad de sus preguntas y de su enseñanza |
| H.8 | Pedro (estudiante) | Recibir sus resultados en cuanto el coordinador los publica | Si llegan tarde, no alcanza a corregir sus errores antes del siguiente examen |
| H.9 | Pedro (estudiante) | Ver en qué preguntas y materias se equivocó | Quiere saber qué reforzar para mejorar su rendimiento |
| H.10 | Pedro (estudiante) | Conocer su posición en el ranking | Compararse con otros lo motiva y le muestra cuánto le falta para alcanzar una vacante |
| H.11 | Ana (estudiante) | Ver su evolución por materia a lo largo de los simulacros | Quiere planificar su estudio según sus debilidades y aprovechar mejor su tiempo |
| H.12 | Ricardo (director) | Contar con estadísticas institucionales oportunas | Debe tomar decisiones estratégicas y hoy recibe información tardía e incompleta |
| H.13 | Ricardo (director) | Comparar el rendimiento entre exámenes y áreas | Necesita saber si la academia mejora para fortalecer su prestigio académico |
| H.14 | Juan (docente) | Adjuntar imágenes y escribir fórmulas en sus preguntas | Matemática, Física y Química plantean problemas con figuras y notación que el texto simple no permite expresar |
| H.15 | Patricia (coordinadora) | Configurar cada examen con pesos y puntajes por pregunta distintos según el área | Cada área (ingenierías, biomédicas, sociales) pondera los ejes y las materias de forma distinta |
| H.16 | Patricia (coordinadora) | Registrar usuarios y asignarles un rol | Debe controlar quién entra al sistema y qué puede hacer cada persona |
| H.17 | Patricia (coordinadora) | Agrupar los exámenes de las áreas en un simulacro | Cada aplicación evalúa a las tres áreas y los resultados deben compararse entre simulacros |
| H.18 | Patricia (coordinadora) | Ver en un panel lo que tiene pendiente | Necesita priorizar lo que bloquea la publicación de resultados |

---

## 2. Diagrama de afinidad (agrupación de historias)

| Grupo | Historia | Usuario | Necesidad | Propósito / Insight |
|---|---|---|---|---|
| **Calificación rápida y confiable** | H.1 | Patricia (coordinadora) | Calificar rápido y sin errores | Reducir el tiempo de trabajo y evitar errores que afecten la confianza |
| | H.2 | Patricia (coordinadora) | Notas y rankings automáticos | Dejar de armarlos a mano y publicarlos a tiempo |
| **Gestión de preguntas y configuración de exámenes** | H.3 | Patricia (coordinadora) | Banco de preguntas organizado y exámenes configurables con versiones | Armar exámenes con pesos y puntajes consistentes |
| | H.4 | Patricia (coordinadora) | Revisar y aprobar preguntas con historial de versiones | Garantizar calidad y trazabilidad |
| | H.6 | Juan (docente) | Enviar preguntas de forma ordenada | Saber qué pasó con sus preguntas |
| | H.14 | Juan (docente) | Adjuntar imágenes y escribir fórmulas | Plantear problemas con figuras y notación científica |
| | H.15 | Patricia (coordinadora) | Configurar el examen con puntajes distintos por área | Ajustar cada examen a la ponderación de su área |
| | H.17 | Patricia (coordinadora) | Agrupar los exámenes de las áreas en un simulacro | Aplicarlos y compararlos juntos |
| **Retroalimentación oportuna al estudiante** | H.8 | Pedro (estudiante) | Resultados en cuanto se publican | Corregir errores antes del siguiente examen |
| | H.9 | Pedro (estudiante) | Ver sus errores por pregunta y materia | Saber qué reforzar |
| | H.10 | Pedro (estudiante) | Conocer su posición en el ranking | Motivarse y medir cuánto le falta |
| | H.11 | Ana (estudiante) | Ver su evolución por materia | Planificar su estudio según sus debilidades |
| **Seguimiento y reportes para decidir** | H.5 | Patricia (coordinadora) | Reportes por examen, área y materia | Supervisar el rendimiento general |
| | H.7 | Juan (docente) | Ver cómo respondieron sus estudiantes | Mejorar sus preguntas y su enseñanza |
| | H.12 | Ricardo (director) | Estadísticas institucionales oportunas | Tomar decisiones estratégicas a tiempo |
| | H.13 | Ricardo (director) | Comparar rendimiento entre exámenes y áreas | Verificar si la academia mejora |
| | H.18 | Patricia (coordinadora) | Ver en un panel lo pendiente | Priorizar el trabajo que bloquea la publicación |
| **Acceso y administración** | H.16 | Patricia (coordinadora) | Registrar usuarios y asignar roles | Controlar quién entra y qué puede hacer |

### Necesidad central de cada grupo

| Grupo | Necesidad central |
|---|---|
| Calificación rápida y confiable | Automatizar la calificación y la generación de resultados para reducir tiempo y errores |
| Gestión de preguntas y configuración de exámenes | Un flujo ordenado para crear, aprobar y reutilizar preguntas, y configurar exámenes con pesos y puntajes consistentes |
| Retroalimentación oportuna al estudiante | Resultados rápidos, con detalle de errores, posición y evolución |
| Seguimiento y reportes para decidir | Información agregada y a tiempo para coordinación, docentes y dirección |
| Acceso y administración | Controlar quién accede al sistema y con qué permisos |


## 3. Precisiones acordadas para la línea base

Las versiones A/B reordenan las mismas preguntas; editar una pregunta aprobada conserva su aprobación y crea una nueva versión activa. Cada estudiante participa en una sola área por simulacro y una segunda cartilla reemplaza la anterior conservando historial. Las marcas múltiples confirmadas valen 0 como blanco. Una recalificación finalizada muestra el nuevo puntaje y actualiza su ranking. Los puntajes no se redondean. El detalle normativo está en `informe_reglas_de_negocio.md` v1.2.

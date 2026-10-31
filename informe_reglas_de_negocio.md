# Informe de reglas de negocio

**Sistema de Gestión de Evaluaciones de Admisión y Seguimiento Académico**
Versión 1.3 — actualizada el 5 de octubre de 2026; incorpora las decisiones confirmadas durante la revisión por casos de uso.

Este informe contiene solo reglas de negocio: políticas, restricciones y condiciones que el sistema debe respetar. Las funciones del sistema (qué puede hacer cada actor) están en el documento de requisitos (`3_requisitos v2.md`) como épicas e historias. Al final hay una tabla con el destino de las reglas anteriores que eran funciones.

---

## 1. Descripción general

El sistema gestiona la preparación académica y la evaluación de estudiantes que participan en procesos de admisión universitaria. Administra estudiantes, docentes, coordinadores, directores, banco de preguntas, exámenes, cartillas físicas, lectura óptica con OpenCV, resultados, ranking, seguimiento del progreso y reportes institucionales.

## 2. Modelo de negocio

**RN-001: Tipo de evaluación** *(antes RN-001 y RN-036)*
El sistema administra evaluaciones de admisión presenciales. El estudiante no desarrolla el examen dentro del sistema.

Flujo real:

1. Preparación académica.
2. Examen físico.
3. Marcado y entrega de la cartilla.
4. Registro de la cartilla.
5. Procesamiento de la imagen con OpenCV (escaneada o fotografiada).
6. Obtención de respuestas.
7. Cálculo de puntaje.
8. Publicación de resultados.

## 3. Actores

Las funciones de cada actor están en el documento de requisitos.

| Actor | Descripción |
|---|---|
| Director | Supervisa la institución a partir de información agregada. |
| Coordinador | Administra los procesos académicos: valida preguntas, configura exámenes y supervisa resultados. |
| Docente | Aporta el contenido académico de sus materias. |
| Estudiante | Participa en la preparación, rinde evaluaciones presenciales y consulta su progreso. |

## 4. Usuarios y roles

**RN-002: Usuarios con múltiples roles** *(antes RN-003)*
Un usuario puede tener varios roles. Ejemplo: un usuario DOCENTE puede pasar a ser DOCENTE y COORDINADOR.

**RN-003: Restricción del estudiante** *(antes RN-004)*
Un estudiante solo puede tener el rol ESTUDIANTE. No puede ser docente, coordinador ni director.

**RN-004: Estudiante sin usuario** *(antes RN-005)*
Un estudiante puede existir sin cuenta de acceso. Si tiene cuenta, esta pertenece únicamente a ese estudiante; el estudiante tiene como máximo una cuenta. Más adelante puede crearse o vincularse su cuenta sin crear otro registro académico.

## 5. Organización académica

**RN-005: Áreas académicas** *(antes RN-008)*
Las áreas de preparación son inicialmente Ingenierías, Biomédicas y Sociales. Cada área puede tener una configuración de examen distinta.

**RN-006: Estructura académica** *(antes RN-009 y RN-010)*
La organización es EJE TEMÁTICO → MATERIA → PREGUNTA.
Los ejes temáticos y las materias son comunes a todas las áreas. Cada pregunta se marca para una o varias áreas. Lo que cambia por área es la configuración del examen (RN-016).
Ejemplo: el eje Matemática tiene las materias Álgebra y Geometría. Álgebra se usa en todas las áreas, y una pregunta de Álgebra puede marcarse para Ingenierías y Biomédicas.

**RN-007: Ciclos y grupos** *(antes RN-011 y RN-012)*
La preparación se organiza en ciclos (por ejemplo PRE 2026-I y PRE 2026-II). Cada ciclo puede tener grupos (por ejemplo mañana y tarde).

**RN-008: Historial de grupo y de área** *(antes RN-013, RN-014 y RN-015)*
Un estudiante puede cambiar de grupo y de área durante su preparación. El sistema conserva el valor anterior, la fecha de inicio, la fecha de cambio y el valor nuevo. Los periodos no se superponen y se interpretan como [inicio, fin): el día del cambio pertenece al nuevo grupo o área. Se admite como máximo un grupo y un área vigentes por estudiante. Las estadísticas por grupo usan el grupo correspondiente a la fecha del examen y al ciclo del simulacro.

**RN-009: Docente y materias** *(antes RN-016)*
Un docente puede estar asociado a una o varias materias. Ejemplo: Pedro, con Álgebra y Geometría, materias del eje Matemática.

## 6. Banco de preguntas

**RN-010: Datos de una pregunta** *(antes RN-020 y RN-021)*
Toda pregunta pertenece a una materia; no puede existir sin ella. Una pregunta contiene:

- la materia asociada (el eje temático se deduce de la materia)
- el área o las áreas para las que se usa
- el docente creador
- el estado de aprobación
- el historial de versiones
- imágenes y fórmulas, de forma opcional, que se conservan con cada versión

**RN-011: Flujo de aprobación** *(antes RN-018 y RN-019)*
La aprobación inicial de una pregunta corresponde al coordinador y registra la versión revisada, el responsable y la fecha. Una persona que tenga los roles DOCENTE y COORDINADOR puede aprobar su propia pregunta.
Estados: BORRADOR → REVISIÓN → APROBADA.

- Una pregunta devuelta por el coordinador vuelve a BORRADOR con su observación.
- Una pregunta APROBADA puede pasar a INACTIVA para retirarla del banco sin eliminarla.
- Una pregunta no puede aprobarse sin tener al menos un área.

**RN-012: Versionamiento de preguntas** *(antes RN-022)*
Una modificación crea una nueva versión y no sobrescribe el contenido anterior. **Editar una pregunta ya aprobada no requiere nueva aprobación.** Su estado continúa APROBADA y solo la nueva versión activa queda disponible para nuevos exámenes. La versión anterior permanece histórica en los exámenes que la utilizaron; no compite como versión activa del banco.
La aprobación inicial no se presenta como una aprobación nueva de cada edición: se conserva la revisión inicial y se registra quién creó cada versión posterior. Las preguntas devueltas que aún no fueron aprobadas siguen el circuito BORRADOR → REVISIÓN → APROBADA.
Cada versión se completa con sus alternativas e imágenes y luego se sella. El contenido sellado no se modifica. La sustitución de la versión activa se realiza en una transacción. Una materia ya asociada a contenido sellado no se cambia: si el contenido corresponde a otra materia, se crea otra pregunta.

**RN-013: Alternativas por versión** *(antes RN-024)*
Las alternativas pertenecen a la versión de la pregunta. Cada versión conserva sus propias alternativas.

**RN-014: Reutilización de preguntas** *(antes RN-023)*
Una pregunta aprobada puede usarse en diferentes exámenes. Al usarla, el examen conserva la versión exacta. Ejemplo: si el examen de enero usó la versión 2, la conserva aunque después exista una versión 3.

## 7. Exámenes de admisión

**RN-015: Examen por área y simulacro** *(antes RN-025 y RN-026)*
Un examen representa una evaluación de admisión dirigida a una sola área. Para evaluar varias áreas se crea un examen por área, cada uno con su propia configuración.
Los exámenes de las áreas se agrupan en un simulacro (una aplicación con nombre y fecha). Un simulacro tiene como máximo un examen por área.

**RN-016: Distribución del examen** *(antes RN-027, RN-028 y RN-029)*
La distribución depende del área y se define por:

- el peso de cada eje temático
- la cantidad de preguntas por materia
- el puntaje por pregunta
- el puntaje de la materia (cantidad de preguntas por puntaje por pregunta)

Se configuran el puntaje total, los pesos **por eje**, la cantidad de preguntas por materia y el puntaje por pregunta. El puntaje de la materia se deriva, no se introduce de forma independiente:

- puntajeMateria = cantidadPreguntas × puntajePregunta.
- sumaPesosEjes = 100 %.
- sumaPuntajesMaterias = puntajeTotal.
- sumaPuntajesMateriasDelEje × 100 = puntajeTotal × pesoEje.

El puntaje por pregunta puede variar por área y materia. Las igualdades deben ser exactas: no se corrigen diferencias redondeando. Cada versión debe cumplir las mismas cantidades y puntajes por materia. La estructura, la fecha y el máximo de un examen aprobado quedan fijos; las correcciones posteriores de clave o política se registran como revisiones independientes.

**RN-017: Puntaje total** *(antes RN-030)*
El examen tiene un puntaje total definido: inicialmente 100 puntos.

**RN-018: Cálculo de puntaje** *(antes RN-031)*
El puntaje depende de la cantidad de preguntas, del puntaje por pregunta de la materia en el área del examen, de las respuestas correctas y de la configuración del examen. Los puntajes configurados, por pregunta y totales conservan hasta 9 decimales en aritmética decimal exacta. No se redondean ni se reducen a 6 decimales al guardar, sumar o ordenar. Un valor con más de 9 decimales se rechaza antes de enviarlo a la base: nunca se aproxima silenciosamente. Los porcentajes son indicadores derivados y no se usan como fuente del puntaje ni del desempate.

**RN-019: Penalización opcional** *(antes RN-032)*
Por defecto la penalización está desactivada: correcta suma su puntaje, incorrecta suma 0, blanco suma 0 y marca múltiple confirmada suma 0. La penalización solo se aplica a una respuesta única incorrecta si el coordinador la configura expresamente. La política adoptada para el total es máximo(0, suma de puntajes): no se publica un puntaje final negativo. La doble marca confirmada se computa como blanco y nunca se penaliza. Cada cambio de política crea una revisión conservada junto al cálculo que la usa.

**RN-020: Versiones de examen y plantilla de respuestas** *(antes RN-033, RN-034 y RN-035)*
Las versiones A y B contienen **las mismas versiones de preguntas y las mismas alternativas**, únicamente cambia el orden de las preguntas. Cada cuadernillo tiene su propia clave por posición. Corregir una clave crea una nueva revisión: no cambia el cuadernillo ni sobrescribe la clave anterior. Cada cálculo identifica su revisión de clave y de política de puntaje.

## 8. Cartillas y lectura óptica

**RN-021: Participación del estudiante** *(antes RN-037 y RN-068)*
El sistema no asigna estudiantes a un examen por adelantado. La participación se determina cuando se recibe la cartilla, se identifica al estudiante y se procesa la información. Un estudiante tiene **como máximo una participación válida, en un solo examen y una sola área por simulacro**. La primera cartilla crea su participación. Recibir otra cartilla del mismo estudiante en ese simulacro reemplaza la anterior para la misma participación; no crea otro intento académico ni permite cambiar al examen de otra área. Se conserva cada recepción, su imagen, el motivo del reemplazo y su responsable; solo una recepción queda vigente. La rectificación excepcional de una asociación administrativa equivocada se rige por RN-039; no permite rendir una segunda área ni sobrescribir la recepción original.

**RN-022: Revisión por baja confianza** *(antes RN-040)*
Una lectura con confianza menor a 80 %, sin confianza calculada o con varias marcas pasa a revisión, aunque la doble marca tenga confianza alta. Si la imagen confirma varias marcas, se conserva esa evidencia y se resuelve como MULTIPLE_CONFIRMADA: respuesta efectiva en blanco y puntaje 0. Revisar la lectura significa transcribir lo observado, nunca sustituirlo por la respuesta correcta de la clave. La anulación de una pregunta no forma parte de este MVP; requiere una regla adicional antes de implementarse.

**RN-023: Reprocesamiento y recalificación** *(antes RN-041 y parte de RN-065)*
Una cartilla puede leerse varias veces y se conservan todos los intentos. Reprocesar una misma imagen y recibir una cartilla de reemplazo son operaciones distintas. Recalificar crea un nuevo cálculo con la cartilla, intento de lectura, clave y política utilizados; no sobrescribe el anterior. Para una participación válida, solo un cálculo es el último vigente. Los cálculos de una asociación invalidada se conservan como históricos y no integran nuevas publicaciones válidas. La vigencia de cálculo es independiente de la publicación. Si el examen ya estaba publicado, al concluir y validar la recalificación se publica automáticamente una nueva edición del resultado y ranking: **el estudiante ve el nuevo puntaje**, sin una segunda acción manual de publicación. Mientras el proceso no termina conserva la última publicación completa; un fallo no expone un resultado parcial.

**RN-024: Corrección manual** *(antes RN-042)*
El coordinador puede corregir manualmente una respuesta detectada. Se registran el valor anterior, el valor nuevo, el usuario que corrigió y el motivo.

## 9. Resultados

**RN-025: Generación de resultados** *(antes RN-043)*
Los resultados se generan solo después de completar el procesamiento de la cartilla: lectura, validación y comparación con la plantilla oficial.

**RN-026: Detalle de respuestas** *(antes RN-045)*
El sistema conserva el detalle de cada pregunta respondida: respuesta marcada, respuesta correcta, si fue correcta y puntaje. Esto permite al estudiante revisar su desempeño.

**RN-027: Estados del resultado** *(antes RN-046)*
Un resultado pasa por los estados CALCULADO → REVISADO → PUBLICADO.

**RN-028: Publicación de resultados** *(antes RN-047)*
La unidad de publicación es el examen de un área dentro de un simulacro. La primera publicación la realiza el coordinador cuando todas las cartillas vigentes tienen resultados revisados. Cada publicación registra responsable, fecha, resultados y posiciones. La comprobación de completitud incluye las entradas de importación pendientes del examen (RN-041), no solo las participaciones identificadas. El estudiante ve su puntaje en la publicación vigente; nunca un cálculo interno incompleto. Una recalificación finalizada sustituye automáticamente esa publicación de forma atómica, conservando las anteriores. Los resultados ajenos no se consultan como detalle personal; el ranking muestra únicamente los datos de comparación autorizados.

## 10. Seguridad y conservación de la información

**RN-029: Control de acceso y separación de responsabilidades** *(antes RN-007, RN-063 y RN-064)*
Cada usuario accede solo a las funciones permitidas según su rol.

- El docente crea contenido.
- El coordinador valida contenido y configura la evaluación.
- El director consulta información institucional.
- El estudiante consulta su información personal. No puede crear ni modificar preguntas, crear exámenes, cambiar configuraciones ni procesar cartillas.

**RN-030: No eliminación de información académica** *(antes RN-048 y RN-065)*
Los datos históricos no se eliminan: resultados, versiones de preguntas, configuraciones de exámenes y procesamientos de cartillas. Quitar un registro significa desactivarlo.

**RN-031: Trazabilidad** *(antes RN-066)*
La trazabilidad obligatoria cubre creación y edición de preguntas, aprobación inicial, recepción y reemplazo de cartillas, procesamientos, correcciones manuales, revisiones de clave/política, cálculos y publicaciones, con responsable y fecha. Las modificaciones se rastrean en las versiones de preguntas (RN-012), las correcciones manuales de lecturas (RN-024), los recálculos de resultados (RN-023) y las fechas de aprobación y publicación.

## 11. Restricciones y alcance

**RN-032: Sin examen en línea** *(antes RN-067)*
El sistema no reemplaza la evaluación física. No incluye preguntas interactivas para resolver en línea, cronómetro de examen ni respuestas ingresadas directamente por los estudiantes.

**RN-033: Una sola institución** *(antes RN-069)*
La primera versión está diseñada para una sola institución. No contempla varias universidades, varios clientes ni configuraciones independientes por institución.

**RN-034: Fuera del alcance de esta versión** *(antes RN-061)*
Esta versión no incluye un módulo de auditoría general ni la generación del examen impreso (PDF) con sus imágenes y fórmulas. Ambos quedan como mejoras futuras.

## 12. Conclusión

El sistema administra la preparación y la evaluación de admisión. Los estudiantes rinden exámenes físicos, las cartillas son la fuente oficial de respuestas y OpenCV automatiza la lectura. Los docentes aportan el contenido, los coordinadores controlan la calidad y la configuración, los directores supervisan los resultados y los estudiantes consultan su progreso. La información histórica se conserva para analizar la evolución, el ranking y la mejora del proceso.

---

## Anexo: reglas anteriores que eran funciones

Estas reglas describían lo que el sistema o un actor hace. Ahora están como historias en `3_requisitos v2.md`.

| Regla anterior | Tema | Dónde está ahora |
|---|---|---|
| RN-002 | Registro de usuarios | HF.1.2, HF.1.3 |
| RN-006 | Información visible del estudiante | HF.5.1.1 a HF.5.1.3, HF.5.2.1, HF.5.2.2 |
| RN-017 | Creación de preguntas | HF.2.1.1 |
| RN-025 (función) | Creación de exámenes | HF.3.1.1 |
| RN-029 (anterior) | Responsable de configurar el examen | HF.3.1.2 |
| RN-036 | Entrega y registro de la cartilla | RN-001, HF.4.1.1 |
| RN-038 | Lectura automática con OpenCV | HF.4.1.2 |
| RN-039 | Nivel de confianza de la lectura | HF.4.1.2, HF.4.1.3, HNF.4.1 |
| RN-043 (flujo) | Cálculo de resultados | HF.4.2.1 |
| RN-044 | Información almacenada del resultado | Modelo de datos (tabla de resultados) |
| RN-049 a RN-052 | Perfil, evolución y progreso por área y materia | HF.5.1.3, HF.5.2.2 |
| RN-053, RN-054 | Generación y tipos de ranking | HF.5.2.1, HF.6.1 |
| RN-055 | Historial de posiciones | HF.5.2.2; posiciones conservadas por publicación |
| RN-056 | Reportes en PDF y Excel | HF.6.4 |
| RN-057 | Reportes del director | HF.6.3 |
| RN-058 | Reportes del coordinador | HF.6.1, HF.6.3 |
| RN-059 | Reportes del docente | HF.6.2 |
| RN-060 | Reportes del estudiante | HF.5.1.1 a HF.5.2.2 |
| RN-063 | Control de acceso por rol | HNF.1.2 |

Queda fuera del MVP el ranking general que mezcla áreas o acumula puntajes de varias fechas. Las estadísticas avanzadas y los reportes de RF.6 se entregan según el plan de releases; los contadores operativos del panel del coordinador sí están incluidos.


## 13. Reglas complementarias consolidadas

**RN-035: Ranking del examen**
El ranking incluye únicamente participantes del mismo examen, área, fecha y simulacro, tomando la publicación vigente. No mezcla exámenes de otros simulacros ni promedia varias fechas para asignar puestos. A/B participan del mismo ranking. En empates exactos se comparte puesto y se deja el salto correspondiente (1, 1, 3). Se conserva el ranking de cada publicación para consultar su historia. Los filtros por materia comparan resultados de esa materia dentro del mismo examen.

**RN-036: Concordancia de referencias**
La versión del cuadernillo debe pertenecer al examen de la cartilla. El resultado debe corresponder al estudiante, examen, versión y cartilla de la participación; su procesamiento pertenece a esa misma cartilla. Cada respuesta de la clave corresponde a una posición real de su cuadernillo. No hay detalles duplicados por posición en un cálculo.

**RN-037: Indicadores sin confundir blancos con errores**
Errores = respuestas únicas incorrectas. Blancos incluye ausencia de marca y marca múltiple confirmada. El porcentaje de error se calcula con incorrectas/total y se informa separado del porcentaje de blancos. Para comparar exámenes con máximos distintos se usan porcentajes en los indicadores comparativos, sin cambiar los puntajes ni mezclar sus rankings.

**RN-038: Alcance mínimo de organización académica**
El coordinador registra, actualiza y desactiva estudiantes, ciclos, grupos, ejes, materias y áreas; asigna materias a docentes y registra cambios de grupo/área con historial. Desactivar impide nuevas asignaciones, pero conserva referencias históricas. No se incluyen matrícula económica, pagos, asistencia ni examen en línea. Estas funciones se desglosan en RF.1 y requieren reestimación de esfuerzo.


## 14. Reglas confirmadas al revisar los casos del coordinador

**RN-039: Rectificación de una asociación equivocada**
El coordinador puede rectificar el estudiante, examen o cuadernillo asociado por error a una cartilla, registrando motivo, evidencia, responsable y fecha. Se conserva la recepción original, se invalida su asociación errónea y se registra la recepción correcta enlazada al origen. Los cálculos anteriores no se transfieren como si fueran resultados de la persona o examen correctos. La operación mantiene como máximo una participación válida por estudiante y simulacro; si ya hay recepción válida en el destino, el coordinador identifica expresamente la que corresponde y documenta cualquier reemplazo. No se borra historia ni se permite otro intento académico.

Una participación sin recepción válida deja de integrar los nuevos resultados y rankings, conservándose históricamente. Se recalculan los exámenes afectados y se reconstruyen sus rankings. Si varios ya estaban publicados, sus ediciones corregidas se activan juntas. Si una rectificación deja a un examen sin participantes válidos, se admite una edición correctiva sin entradas que conserve el motivo; esto no autoriza publicar inicialmente un examen ordinario vacío.

**RN-040: Recepción inicial tardía**
Se puede registrar, después de publicar, la primera cartilla de un estudiante que sí rindió ese examen, con motivo y responsable. Se conserva la restricción de una sola participación válida/área por simulacro. La cartilla se identifica, lee, revisa y califica con las reglas vigentes del examen. Al completar y validar el nuevo conjunto de resultados, se genera automáticamente una edición completa que incluye al participante y actualiza el ranking. Hasta entonces se conserva la última edición completa.

**RN-041: Entradas de importación pendientes y resolución trazable**
Cada imagen o página recibida conserva su origen y estado aun si todavía no permite identificar estudiante o A/B. No se crea una participación suponiendo su identidad. Las entradas pendientes de identificación, con error o esperando reemplazo impiden declarar completos los resultados del examen de destino.

Una imagen ilegible espera reemplazo legible y no se computa como blanco ni como cero. Se conserva el origen y el enlace al reemplazo. Una entrada duplicada o ajena puede descartarse justificadamente, con motivo, responsable, fecha y evidencia conservada. Si ya originó una recepción académica, se corrige mediante reemplazo o rectificación; no se elude esa historia descartando el archivo. Reintentar una carga no constituye por sí mismo una recepción nueva. No se exige un padrón de estudiantes asignados por adelantado.

**RN-042: Participación sin grupo y corrección del historial académico**
Un estudiante registrado puede rendir sin grupo vigente en el ciclo del simulacro; en las estadísticas figura como «sin grupo». El área del resultado es la del examen rendido, no una inferencia del grupo actual.

El coordinador puede rectificar el historial académico con motivo, responsable y fecha, conservando los valores anteriores y corregidos y validando periodos sin superposición. Las estadísticas nuevas usan el historial rectificado. Una corrección administrativa de grupo no modifica puntajes, posiciones ni ediciones ya publicadas. Los reportes nuevos identifican su fecha de generación; los documentos ya exportados conservan su contenido histórico.

**RN-043: Conjunto coherente de calificación**
Para calcular se identifica un conjunto confirmado e inmutable de revisiones de clave A/B y política. Las claves por posición deben concordar para los mismos ítems, sin posiciones duplicadas/faltantes ni alternativas inexistentes. Activar un nuevo conjunto no sobrescribe revisiones anteriores ni cambia resultados publicados sin recalcular y validar. La importación de Excel se previsualiza y valida completa; un fallo no sustituye la configuración anterior.

**RN-044: Revisión, vigencia y entrega completa**
El coordinador puede consultar cálculos aún no publicados y registrar su revisión con responsable y fecha. Una entrega de resultados contiene todas las participaciones válidas del examen y sus cálculos revisados, con las cartillas, lecturas y conjunto aplicables. Un cambio relevante invalida una entrega anterior que ya no corresponde a las entradas actuales. Solo se reutilizan cálculos si sus entradas y conjunto siguen coincidiendo.

Los fallos de publicación no exponen ediciones parciales ni cambian la edición vigente. Se conserva la publicación pendiente para reintentar sin duplicar ediciones y nunca activar una entrega obsoleta sobre una más reciente. Puntaje, detalle y puesto consultados corresponden a una misma edición. Estas reglas son independientes del mecanismo técnico elegido para transacciones y reintentos.

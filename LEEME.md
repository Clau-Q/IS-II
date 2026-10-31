# Sistema de Gestión de Exámenes y Rendimiento Académico

Línea base corregida el 3 de octubre de 2026, previa al modelado DDD.

1. [Reglas de negocio vigentes](informe_reglas_de_negocio.md): políticas y restricciones, versión 1.2.
2. [Requisitos vigentes](<3_requisitos v2.md>): historias, alcance y planificación pendiente de reestimación.
3. [Correcciones y criterios](7_correcciones_y_criterios.md): decisiones, escenarios y responsabilidades de la futura aplicación.
4. [Diseño SQL](nueva_base_de_datos.sql): instalación nueva; no aplicar como migración sobre datos existentes.
5. [Validación realizada](VALIDACION.md): resultados y límites de las pruebas.

Los documentos 1, 2, 4 y 5 conservan el contexto, necesidades, mapas y flujos. El documento 6 es la revisión histórica inicial. Los originales previos a las correcciones están en `historial/antes_correcciones_2026-10-03`.

Los HTML son prototipos de pantalla, no una aplicación conectada a la base de datos. El modelo DDD aún no se ha elaborado.

## Prototipo unificado — 5 de octubre de 2026

[PROTOTIPO_COMPLETO.html](PROTOTIPO_COMPLETO.html) organiza las ventanas en pestañas: Inicio de sesión (común), Coordinador, Estudiante, Docente y Director. Solo se muestran las ventanas del perfil seleccionado, con un índice propio. Hay 26 ventanas: la pantalla de reportes tiene una presentación separada para Coordinador y Director. Todo el CSS está en una etiqueta `style` en la cabecera y el HTML debajo; se abre directamente en el navegador sin dependencias externas. Los archivos de origen se conservan.

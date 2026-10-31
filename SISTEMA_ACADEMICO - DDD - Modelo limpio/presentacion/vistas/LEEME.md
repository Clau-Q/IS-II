# Ventanas HTML del Sistema de Examen de Admisión

Abrir `index.html` para elegir entre la aplicación de referencia y los prototipos de requisitos.

## Interfaz de la aplicación

`comun/inicio_de_sesion.html` reproduce `VentanaLogin`. Al ingresar abre `administracion/panel.html`, que reproduce las ventanas de la aplicación Flet: cabecera, usuario, menú lateral y las secciones Inicio, Configuración, Configurar Respuestas, Procesar Hojas, Resultados, Estadísticas y Estudiantes. Los estilos y recursos compartidos están en `recursos/`, y conservan las constantes de `src/assets` de la versión Flet: rojo `#FF0000`, rojo claro `#FFE8E8`, grises, bordes, radios y sombras.

## Paneles por rol

Cada carpeta de rol tiene un `panel.html` propio, con cabecera, navegación lateral y contenido alineado a sus casos de uso:

- `coordinador/panel.html`: estudiantes, simulacros, preguntas, cartillas y reportes.
- `director/panel.html`: indicadores institucionales, comparativos y reportes.
- `docente/panel.html`: preguntas, creación de preguntas y estadísticas de materias.
- `estudiante/panel.html`: resultado, detalle por pregunta, ranking y evolución.

## Prototipos de requisitos

Las carpetas `comun`, `coordinador`, `estudiante`, `docente` y `director` conservan las 26 pantallas derivadas de `PROTOTIPO_COMPLETO.html`, organizadas por perfil. Son una referencia complementaria para las capacidades del sistema DDD.

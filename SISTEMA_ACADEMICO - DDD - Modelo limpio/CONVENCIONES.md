# Convenciones de nombres de Python

- Paquetes y módulos: minúsculas y `snake_case` (por ejemplo, `estudiante_app_service.py`).
- Clases: `PascalCase` (por ejemplo, `EstudianteAppService`). Se conservan las siglas DTO, ORM y los nombres de tecnologías en las clases existentes.
- Métodos, parámetros y atributos: `snake_case`.
- Constantes y miembros de enumeraciones: `MAYUSCULAS_CON_GUIONES_BAJOS`.
- Contratos existentes: se conserva el prefijo I en las clases; sus módulos usan `i_`, por ejemplo `i_estudiante_repositorio.py` / `IEstudianteRepositorio`.
- Los archivos `__init__.py` identifican los paquetes. Las importaciones internas usan el nombre exacto del módulo, incluidas sus minúsculas.
- Los nombres del dominio permanecen en español. Cada módulo conserva el nombre de la clase que representa, convertido a snake_case.

Ejemplos de las capas:

| Módulo | Clase |
| --- | --- |
| `dominio/organizacion_academica/estudiante.py` | `Estudiante` |
| `aplicacion/servicios/estudiante_app_service.py` | `EstudianteAppService` |
| `infraestructura/persistencia/repositories/estudiante_orm_repositorio.py` | `EstudianteORMRepositorio` |
| `presentacion/controllers/estudiante_controller.py` | `EstudianteController` |

Esta normalización modifica nombres, importaciones y firmas redundantes. No implementa casos de uso ni crea bases de datos. Los métodos pendientes conservan su estado actual.

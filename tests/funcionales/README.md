# Pruebas funcionales de identidad y acceso

Laboratorio 06. Python, Selenium WebDriver y unittest.
Once casos diseñados con clases de equivalencia y casos de uso.

## Instalación

Desde la raíz del repositorio, con el entorno virtual del proyecto:

    .\.venv-1\Scripts\python.exe -m pip install -r Sistema_Academico\requirements.txt
    .\.venv-1\Scripts\python.exe -m pip install -r tests\funcionales\requirements.txt

## Ejecución

    .\.venv-1\Scripts\python.exe -B tests\funcionales\ejecutar.py

Resultado: tests/funcionales/reportes/ejecucion.txt.
La tabla de casos y la captura del reporte se presentan en el informe del
Laboratorio 06.

## Archivos necesarios

- test_acceso_web.py: casos Selenium con setUp y tearDown.
- _aplicacion_prueba.py: servidor Flask y cuentas temporales.
- ejecutar.py: ejecución y reporte de unittest.
- requirements.txt: dependencia de Selenium.
- reportes/ejecucion.txt: evidencia de ejecución.

Chrome funciona sin ventana. Selenium Manager puede necesitar Internet para
obtener el controlador. Se usan rutas, vistas, servicios y protector reales.
SQLite temporal sustituye MySQL; no se modifican datos existentes.
Las cuentas temporales usan Prueba123!, no una contraseña de MySQL.
CSRF permanece activo. Estas pruebas no validan el dialecto MySQL.

# Sistema académico

Aplicación Flask con MySQL. El programa está en `SISTEMA_ACADEMICO - DDD - Modelo limpio`.

## Ejecutar

1. Instala Python y MySQL. Para una instalación nueva, ejecuta `nueva_base_de_datos.sql` en MySQL.
2. Desde la raíz del proyecto, instala las dependencias:

   ```powershell
   .\.venv-1\Scripts\python.exe -m pip install -r ".\SISTEMA_ACADEMICO - DDD - Modelo limpio\requirements.txt"
   ```

3. Guarda la contraseña de MySQL en `mysql_clave.local`, dentro de la carpeta del programa, o configura `SISTEMA_MYSQL_PASSWORD`.
4. Inicia la aplicación:

   ```powershell
   .\.venv-1\Scripts\python.exe ".\SISTEMA_ACADEMICO - DDD - Modelo limpio\run.py"
   ```

Abre http://127.0.0.1:5000/. La conexión local usa MySQL en `localhost:3306`, usuario `root` y base `sistema_evaluacion`.

Si necesitas crear el entorno virtual, ejecuta `python -m venv .venv-1` desde la raíz.

Las actualizaciones de bases existentes están en `infraestructura/persistencia/*.sql`. Las imágenes cargadas se conservan en `datos_privados` dentro del programa. Las credenciales, el entorno virtual y los archivos privados se excluyen de Git.

# Ejecutar el sistema de prueba

Desde esta carpeta, con el entorno virtual activado, ejecuta:

```powershell
python run.py
```

Después abre `http://127.0.0.1:5000/`. Para detener el servidor, pulsa Ctrl+C. Si faltan dependencias, instálalas una vez con `python -m pip install -r requirements.txt`.

El archivo `run.py` conecta con la base MySQL de prueba `sistema_evaluacion` en `localhost:3306` usando el usuario `root`. La contraseña se obtiene del archivo local `mysql_clave.local`, que no se incluye en Git, o de la variable de entorno `SISTEMA_MYSQL_PASSWORD`. La base se crea con `../nueva_base_de_datos.sql`.

Las cuentas de prueba `coordinador`, `director`, `docente` y `estudiante` usan la contraseña `miclave`. Por ahora están conectados los paneles de coordinador y director.

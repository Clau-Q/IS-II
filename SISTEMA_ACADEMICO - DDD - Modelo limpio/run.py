"""Inicio local del sistema académico con la base MySQL de prueba."""
import os
import sys
from pathlib import Path


def main():
    try:
        from sqlalchemy import create_engine, text
        from sqlalchemy.engine import URL
        from sqlalchemy.exc import SQLAlchemyError
        from app import crear_app
    except ModuleNotFoundError as error:
        print(f"Falta la dependencia {error.name}. Instala las dependencias con: python -m pip install -r requirements.txt")
        return 1

    archivo_clave = Path(__file__).with_name("mysql_clave.local")
    clave = os.environ.get("SISTEMA_MYSQL_PASSWORD")
    if clave is None and archivo_clave.is_file():
        clave = archivo_clave.read_text(encoding="utf-8").strip()
    if clave is None:
        print("Configura SISTEMA_MYSQL_PASSWORD o crea mysql_clave.local con la contraseña de MySQL.")
        return 1
    url = URL.create(
        "mysql+pymysql", username="root", password=clave,
        host="localhost", port=3306, database="sistema_evaluacion",
        query={"charset": "utf8mb4"},
    )
    os.environ["SISTEMA_DATABASE_URL"] = url.render_as_string(hide_password=False)
    print("Conectando a MySQL: localhost:3306, base sistema_evaluacion...")
    motor = create_engine(url, pool_pre_ping=True, hide_parameters=True)
    try:
        with motor.connect() as conexion:
            conexion.execute(text("SELECT id_usuario, username, password_hash, nombres, estado FROM usuarios LIMIT 0"))
            conexion.execute(text("SELECT r.nombre FROM roles r JOIN usuario_roles ur ON ur.id_rol = r.id_rol LIMIT 0"))
    except SQLAlchemyError as error:
        print("No se pudo conectar a MySQL o no se encontraron las tablas de acceso.")
        print(f"Tipo de error: {type(error).__name__}")
        return 1
    finally:
        motor.dispose()

    print("Conexión establecida. Abre http://127.0.0.1:5000/ en el navegador.")
    print("Para detener el servidor, pulsa Ctrl+C.")
    crear_app().run(host="127.0.0.1", port=5000, debug=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())

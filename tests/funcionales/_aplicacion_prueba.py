"""Servidor del sistema académico con cuentas temporales para Selenium."""
import os
import sys
import threading
from pathlib import Path
from unittest.mock import patch

from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from werkzeug.serving import make_server

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "Sistema_Academico"))
from app import crear_app
from aplicacion.servicios.cuenta_usuario_app_service import CuentaUsuarioAppService
from infraestructura.persistencia.repositories.cuenta_usuario_orm_repositorio import CuentaUsuarioORMRepositorio
from infraestructura.seguridad.protector_credenciales_werkzeug import ProtectorCredencialesWerkzeug

CLAVE = "Prueba123!"


class AplicacionPrueba:
    def iniciar(self):
        self.motor = create_engine(
            "sqlite+pysqlite:///:memory:",
            connect_args={"check_same_thread": False}, poolclass=StaticPool
        )
        protector = ProtectorCredencialesWerkzeug()
        with self.motor.begin() as c:
            c.execute(text("""CREATE TABLE usuarios (
                id_usuario INTEGER PRIMARY KEY, username TEXT UNIQUE,
                password_hash TEXT, nombres TEXT, estado TEXT)"""))
            c.execute(text("CREATE TABLE roles (id_rol INTEGER PRIMARY KEY, nombre TEXT)"))
            c.execute(text("CREATE TABLE usuario_roles (id_usuario INTEGER, id_rol INTEGER)"))
            c.execute(text("INSERT INTO roles VALUES (1,'COORDINADOR'),(2,'DOCENTE')"))
            c.execute(text("""INSERT INTO usuarios VALUES
                (1,'coordinador_prueba',:clave,'Ana','ACTIVO'),
                (2,'inactivo_prueba',:clave,'Luis','INACTIVO'),
                (3,'multi_prueba',:clave,'Maria','ACTIVO')"""),
                {"clave": protector.generar_hash(CLAVE)})
            c.execute(text("INSERT INTO usuario_roles VALUES (1,1),(2,1),(3,1),(3,2)"))
        servicio = CuentaUsuarioAppService(CuentaUsuarioORMRepositorio(self.motor), protector)

        with patch.dict(os.environ, {"SISTEMA_DATABASE_URL": ""}):
            self.app = crear_app(servicio_prueba=servicio)
        self.servidor = make_server("127.0.0.1", 0, self.app)
        self.url = "http://127.0.0.1:" + str(self.servidor.server_port)
        self.hilo = threading.Thread(target=self.servidor.serve_forever, daemon=True)
        self.hilo.start()

    def detener(self):
        if hasattr(self, "servidor"):
            self.servidor.shutdown()
            self.servidor.server_close()
            self.hilo.join(timeout=3)
        if hasattr(self, "motor"):
            self.motor.dispose()

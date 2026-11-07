"""Soporte de pruebas: imports y base SQLite temporal, sin acceder a MySQL."""
import sys
from pathlib import Path

from sqlalchemy import create_engine, text

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "Sistema_Academico"))


class BaseSQLite:
    def setUp(self):
        self.motor = create_engine("sqlite+pysqlite:///:memory:")
        self.addCleanup(self.motor.dispose)
        with self.motor.begin() as conexion:
            conexion.execute(text("""
                CREATE TABLE usuarios (
                    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    nombres TEXT NOT NULL,
                    apellidos TEXT NOT NULL,
                    estado TEXT NOT NULL
                )
            """))
            conexion.execute(text(
                "CREATE TABLE roles (id_rol INTEGER PRIMARY KEY, nombre TEXT UNIQUE)"
            ))
            conexion.execute(text("""
                CREATE TABLE usuario_roles (
                    id_usuario INTEGER NOT NULL, id_rol INTEGER NOT NULL,
                    UNIQUE(id_usuario, id_rol)
                )
            """))
            conexion.execute(text(
                "CREATE TABLE docentes (id_usuario INTEGER UNIQUE NOT NULL)"
            ))
            conexion.execute(text(
                "INSERT INTO roles(id_rol,nombre) VALUES "
                "(1,'DOCENTE')"
            ))

    def consultar(self, sql, parametros=None):
        with self.motor.connect() as conexion:
            return conexion.execute(text(sql), parametros or {}).mappings().all()

import unittest
from unittest.mock import MagicMock
import _soporte  # Configura los imports de la aplicación.
from sqlalchemy.engine import Connection, Engine
from infraestructura.persistencia.repositories.cuenta_usuario_orm_repositorio import CuentaUsuarioORMRepositorio
from infraestructura.persistencia.repositories.gestion_usuarios_repositorio import GestionUsuariosRepositorio


class TestCuentaUsuarioRepositorio(unittest.TestCase):

    def setUp(self):
        self.motor = MagicMock(spec=Engine)
        self.conexion = MagicMock(spec=Connection)
        self.motor.connect.return_value.__enter__.return_value = self.conexion
        self.repositorio = CuentaUsuarioORMRepositorio(self.motor)
        self.fila = {
            "id_usuario": 7, "username": "ana", "nombres": "Ana",
            "password_hash": "hash-seguro", "estado": "ACTIVO"
        }

    def test_busqueda_devuelve_datos_y_roles_de_la_cuenta(self):
        # Inicializar
        usuario = MagicMock()
        usuario.mappings.return_value.first.return_value = self.fila
        roles = MagicMock()
        roles.scalars.return_value.all.return_value = ["DOCENTE", "COORDINADOR"]
        self.conexion.execute.side_effect = [usuario, roles]

        # Ejecutar
        resultado = self.repositorio.buscar_por_nombre("ana")

        # Verificar
        self.assertEqual(resultado, {
            "id": 7, "usuario": "ana", "nombre": "Ana",
            "password_hash": "hash-seguro", "activa": True,
            "roles": ["DOCENTE", "COORDINADOR"]
        })
        self.assertEqual(self.conexion.execute.call_args_list[0].args[1], {"nombre": "ana"})
        self.assertEqual(self.conexion.execute.call_args_list[1].args[1], {"id": 7})

    def test_cuenta_inexistente_no_consulta_roles(self):
        # Inicializar
        self.conexion.execute.return_value.mappings.return_value.first.return_value = None

        # Ejecutar
        resultado = self.repositorio.buscar_por_nombre("inexistente")

        # Verificar
        self.assertIsNone(resultado)
        self.conexion.execute.assert_called_once()


    def test_cuenta_inactiva_se_mapea_como_inactiva(self):
        # Inicializar
        self.fila["estado"] = "INACTIVO"
        usuario = MagicMock()
        usuario.mappings.return_value.first.return_value = self.fila
        roles = MagicMock()
        roles.scalars.return_value.all.return_value = []
        self.conexion.execute.side_effect = [usuario, roles]

        # Ejecutar
        resultado = self.repositorio.buscar_por_nombre("ana")

        # Verificar
        self.assertFalse(resultado["activa"])
        self.assertEqual(resultado["roles"], [])

class TestGestionUsuariosRepositorio(unittest.TestCase):

    def setUp(self):
        self.motor = MagicMock(spec=Engine)
        self.conexion = MagicMock(spec=Connection)
        self.motor.connect.return_value.__enter__.return_value = self.conexion
        self.motor.begin.return_value.__enter__.return_value = self.conexion
        self.repositorio = GestionUsuariosRepositorio(self.motor)

    def test_listar_devuelve_las_filas_consultadas(self):
        # Inicializar
        filas = [{"id_usuario": 7, "username": "ana", "roles": "DOCENTE"}]
        self.conexion.execute.return_value.mappings.return_value.all.return_value = filas

        # Ejecutar
        resultado = self.repositorio.listar()

        # Verificar
        self.assertEqual(resultado, filas)
        self.motor.connect.return_value.__exit__.assert_called_once()


    def test_cambia_estado_de_cuenta_normal(self):
        # Inicializar
        self.conexion.execute.return_value.mappings.return_value.first.return_value = {
            "username": "ana", "es_director": False
        }

        # Ejecutar
        self.repositorio.estado(7, "INACTIVO", False)

        # Verificar
        self.assertEqual(self.conexion.execute.call_count, 2)
        actualizacion = self.conexion.execute.call_args
        self.assertIn("UPDATE usuarios", str(actualizacion.args[0]))
        self.assertEqual(actualizacion.args[1], {"id": 7, "estado": "INACTIVO"})

    def test_estado_rechaza_cuenta_inexistente_sin_actualizar(self):
        # Inicializar
        self.conexion.execute.return_value.mappings.return_value.first.return_value = None

        # Ejecutar y verificar
        with self.assertRaisesRegex(ValueError, "La cuenta no existe"):
            self.repositorio.estado(99, "INACTIVO", True)
        self.conexion.execute.assert_called_once()

    def test_no_permite_cambiar_roles_de_la_propia_cuenta(self):
        # Inicializar
        self.conexion.execute.return_value.mappings.return_value.first.return_value = {
            "id_usuario": 7, "es_director": False
        }

        # Ejecutar y verificar
        with self.assertRaisesRegex(ValueError, "propia cuenta"):
            self.repositorio.cambiar_roles(7, ["DOCENTE"], True, 7)
        self.conexion.execute.assert_called_once()

if __name__ == "__main__":
    unittest.main()

import unittest
from unittest.mock import Mock
import _soporte  # Configura los imports de la aplicación.
from aplicacion.puertos.i_protector_credenciales import IProtectorCredenciales
from aplicacion.servicios.cuenta_usuario_app_service import CuentaUsuarioAppService
from aplicacion.servicios.gestion_usuarios_app_service import GestionUsuariosAppService
from dominio.identidad_acceso.i_cuenta_repositorio import ICuentaRepositorio
from infraestructura.persistencia.repositories.gestion_usuarios_repositorio import GestionUsuariosRepositorio


class TestCuentaUsuarioAppService(unittest.TestCase):

    def setUp(self):
        self.repositorio = Mock(spec_set=ICuentaRepositorio)
        self.protector = Mock(spec_set=IProtectorCredenciales)
        self.servicio = CuentaUsuarioAppService(self.repositorio, self.protector)
        self.cuenta = {
            "id": 7, "usuario": "ana", "password_hash": "hash-seguro",
            "activa": True, "roles": ["DOCENTE"]
        }

    def test_inicia_sesion_y_verifica_hash_con_la_credencial(self):
        # Inicializar
        self.repositorio.buscar_por_nombre.return_value = self.cuenta
        self.protector.verificar.return_value = True

        # Ejecutar
        resultado = self.servicio.iniciar_sesion("ana", "Clave123!")

        # Verificar
        self.assertIs(resultado, self.cuenta)
        self.repositorio.buscar_por_nombre.assert_called_once_with("ana")
        self.protector.verificar.assert_called_once_with("hash-seguro", "Clave123!")

    def test_cuenta_inactiva_no_verifica_contrasena(self):
        # Inicializar
        self.cuenta["activa"] = False
        self.repositorio.buscar_por_nombre.return_value = self.cuenta

        # Ejecutar
        resultado = self.servicio.iniciar_sesion("ana", "Clave123!")

        # Verificar
        self.assertIsNone(resultado)
        self.protector.verificar.assert_not_called()

    def test_rechaza_contrasena_incorrecta(self):
        # Inicializar
        self.repositorio.buscar_por_nombre.return_value = self.cuenta
        self.protector.verificar.return_value = False

        # Ejecutar
        resultado = self.servicio.iniciar_sesion("ana", "incorrecta")

        # Verificar
        self.assertIsNone(resultado)
        self.protector.verificar.assert_called_once_with("hash-seguro", "incorrecta")


    def test_usuario_inexistente_no_verifica_contrasena(self):
        # Inicializar
        self.repositorio.buscar_por_nombre.return_value = None

        # Ejecutar
        resultado = self.servicio.iniciar_sesion("nadie", "Clave123!")

        # Verificar
        self.assertIsNone(resultado)
        self.protector.verificar.assert_not_called()

    def test_consulta_devuelve_cuenta_activa(self):
        # Inicializar
        self.repositorio.buscar_por_nombre.return_value = self.cuenta

        # Ejecutar
        resultado = self.servicio.consultar_cuenta_activa("ana")

        # Verificar
        self.assertIs(resultado, self.cuenta)
        self.repositorio.buscar_por_nombre.assert_called_once_with("ana")
        self.protector.verificar.assert_not_called()

class TestGestionUsuariosAppService(unittest.TestCase):

    def setUp(self):
        self.repositorio = Mock(spec_set=GestionUsuariosRepositorio)
        self.protector = Mock(spec_set=IProtectorCredenciales)
        self.protector.generar_hash.return_value = "hash-seguro"
        self.servicio = GestionUsuariosAppService(self.repositorio, self.protector)
        self.formulario = {
            "username": " ana ", "nombres": " Ana ", "apellidos": " Perez ",
            "contrasena": "Clave123!", "roles": ["DOCENTE"]
        }

    def test_crea_usuario_con_datos_normalizados_y_clave_protegida(self):
        # Inicializar
        formulario = self.formulario

        # Ejecutar
        self.servicio.crear(formulario, director=False)

        # Verificar
        self.protector.generar_hash.assert_called_once_with("Clave123!")
        self.repositorio.crear.assert_called_once_with(
            {"username": "ana", "nombres": "Ana", "apellidos": "Perez"},
            "hash-seguro", ["DOCENTE"]
        )

    def test_rechaza_contrasena_de_siete_caracteres(self):
        # Inicializar
        self.formulario["contrasena"] = "1234567"

        # Ejecutar y verificar
        with self.assertRaises(ValueError):
            self.servicio.crear(self.formulario, director=False)
        self.repositorio.crear.assert_not_called()
        self.protector.generar_hash.assert_not_called()


    def test_rechaza_username_vacio_sin_persistir(self):
        # Inicializar
        self.formulario["username"] = "   "

        # Ejecutar y verificar
        with self.assertRaises(ValueError):
            self.servicio.crear(self.formulario, director=False)
        self.repositorio.crear.assert_not_called()
        self.protector.generar_hash.assert_not_called()

    def test_estado_invalido_no_se_envia_al_repositorio(self):
        # Inicializar
        estado = "BLOQUEADO"

        # Ejecutar y verificar
        with self.assertRaises(ValueError):
            self.servicio.cambiar_estado(7, estado, director=True)
        self.repositorio.estado.assert_not_called()

    def test_cambiar_roles_delega_roles_y_actor(self):
        # Inicializar
        roles = ["DOCENTE", "COORDINADOR"]

        # Ejecutar
        self.servicio.cambiar_roles(7, roles, director=False, actor=99)

        # Verificar
        self.repositorio.cambiar_roles.assert_called_once_with(
            7, ["DOCENTE", "COORDINADOR"], False, 99
        )

if __name__ == "__main__":
    unittest.main()

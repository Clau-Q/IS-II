import unittest

from Sistema_Academico.dominio.identidad_acceso.cuenta_usuario import CuentaUsuario


class TestEstadoCuentaUsuario(unittest.TestCase):

    def test_activar_cuenta(self):
        # Inicializar
        cuenta = CuentaUsuario()
        cuenta.activa = False

        # Ejecutar
        cuenta.activar()

        # Verificar
        self.assertTrue(cuenta.activa)

    def test_desactivar_cuenta(self):
        # Inicializar
        cuenta = CuentaUsuario()
        cuenta.activa = True

        # Ejecutar
        cuenta.desactivar()

        # Verificar
        self.assertFalse(cuenta.activa)


if __name__ == "__main__":
    unittest.main()

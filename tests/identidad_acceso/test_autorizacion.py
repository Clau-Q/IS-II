import unittest
from Sistema_Academico.dominio.identidad_acceso.autorizacion import Autorizacion


class TestAccesoPorRol(unittest.TestCase):

    def test_permite_acceso_con_rol_requerido(self):
        # Inicializar
        roles = ["DOCENTE"]
        requerido = "DOCENTE"

        # Ejecutar
        resultado = Autorizacion.puede_acceder(roles, requerido)

        # Verificar
        self.assertTrue(resultado)

    def test_deniega_acceso_sin_rol_requerido(self):
        # Inicializar
        roles = ["ESTUDIANTE"]
        requerido = "DIRECTOR"

        # Ejecutar
        resultado = Autorizacion.puede_acceder(roles, requerido)

        # Verificar
        self.assertFalse(resultado)

    def test_director_puede_acceder_como_coordinador(self):
        # Inicializar
        roles = ["DIRECTOR"]
        requerido = "COORDINADOR"

        # Ejecutar
        resultado = Autorizacion.puede_acceder(roles, requerido)

        # Verificar
        self.assertTrue(resultado)

class TestValidacionRoles(unittest.TestCase):

    def test_rechaza_roles_vacios(self):
        # Inicializar
        roles = []
        director = True

        # Ejecutar y verificar: debe lanzar ValueError
        with self.assertRaises(ValueError):
            Autorizacion.validar_roles(roles, director)


    def test_acepta_rol_docente(self):
        # Inicializar
        roles = ["DOCENTE"]
        director = False

        # Ejecutar
        resultado = Autorizacion.validar_roles(roles, director)

        # Verificar
        self.assertIsNone(resultado)

    def test_rechaza_roles_duplicados(self):
        # Inicializar
        roles = ["DOCENTE", "DOCENTE"]
        director = True

        # Ejecutar y verificar
        with self.assertRaises(ValueError):
            Autorizacion.validar_roles(roles, director)

    def test_rechaza_estudiante_combinado_con_docente(self):
        # Inicializar
        roles = ["ESTUDIANTE", "DOCENTE"]
        director = True

        # Ejecutar y verificar
        with self.assertRaises(ValueError):
            Autorizacion.validar_roles(roles, director)

    def test_solo_director_puede_asignar_rol_director(self):
        # Inicializar
        roles = ["DIRECTOR"]
        director = False

        # Ejecutar y verificar
        with self.assertRaises(PermissionError):
            Autorizacion.validar_roles(roles, director)


    def test_rechaza_rol_desconocido(self):
        # Inicializar
        roles = ["ADMINISTRADOR"]
        director = True

        # Ejecutar y verificar
        with self.assertRaises(ValueError):
            Autorizacion.validar_roles(roles, director)


class TestModificacionCuenta(unittest.TestCase):

    def test_no_director_no_puede_modificar_cuenta_de_director(self):
        # Inicializar
        es_director = True
        actor_director = False

        # Ejecutar y verificar
        with self.assertRaises(PermissionError):
            Autorizacion.validar_modificacion_cuenta(
                es_director, actor_director
            )


if __name__ == "__main__":
    unittest.main()

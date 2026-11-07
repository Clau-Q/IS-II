import unittest
from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from _aplicacion_prueba import AplicacionPrueba, CLAVE


class TestAccesoWeb(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.aplicacion = AplicacionPrueba()
        cls.addClassCleanup(cls.aplicacion.detener)
        cls.aplicacion.iniciar()

    def setUp(self):
        opciones = webdriver.ChromeOptions()
        opciones.add_argument("--headless=new")
        opciones.add_argument("--window-size=1280,900")
        self.driver = webdriver.Chrome(options=opciones)
        self.espera = WebDriverWait(self.driver, 8)
        self.driver.get(self.aplicacion.url)

    def tearDown(self):
        self.driver.quit()

    def ingresar(self, usuario, clave):
        self.driver.find_element(By.NAME, "usuario").send_keys(usuario)
        self.driver.find_element(By.NAME, "contrasena").send_keys(clave)
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    def aviso(self):
        return self.espera.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "[role='alert']"))).text

    def test_01_muestra_formulario(self):
        # Ejecutar y verificar
        self.assertEqual(self.driver.title, "Iniciar sesión")
        self.assertTrue(self.driver.find_element(By.NAME, "usuario").is_displayed())
        self.assertTrue(self.driver.find_element(By.NAME, "contrasena").is_displayed())

    def test_02_credenciales_validas(self):
        # Inicializar
        usuario = "coordinador_prueba"
        # Ejecutar
        self.ingresar(usuario, CLAVE)
        # Verificar
        self.espera.until(EC.url_contains("/coordinador"))
        self.assertIn("Coordinador", self.driver.find_element(By.CLASS_NAME, "user-chip").text)

    def test_03_contrasena_incorrecta(self):
        # Inicializar
        usuario, clave = "coordinador_prueba", "incorrecta"
        # Ejecutar
        self.ingresar(usuario, clave)
        # Verificar
        self.assertIn("Usuario o contraseña incorrectos", self.aviso())
        self.assertEqual(urlparse(self.driver.current_url).path, "/")

    def test_04_usuario_inexistente(self):
        # Inicializar
        usuario = "no_existe"
        # Ejecutar
        self.ingresar(usuario, CLAVE)
        # Verificar
        self.assertIn("Usuario o contraseña incorrectos", self.aviso())

    def test_05_cuenta_inactiva(self):
        # Inicializar
        usuario = "inactivo_prueba"
        # Ejecutar
        self.ingresar(usuario, CLAVE)
        # Verificar
        self.assertIn("cuenta inactiva", self.aviso())

    def test_06_usuario_obligatorio(self):
        # Inicializar
        campo = self.driver.find_element(By.NAME, "usuario")
        self.driver.find_element(By.NAME, "contrasena").send_keys(CLAVE)
        # Ejecutar
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        # Verificar
        self.assertTrue(campo.get_property("validationMessage"))
        self.assertEqual(urlparse(self.driver.current_url).path, "/")

    def test_07_contrasena_obligatoria(self):
        # Inicializar
        self.driver.find_element(By.NAME, "usuario").send_keys("coordinador_prueba")
        campo = self.driver.find_element(By.NAME, "contrasena")
        # Ejecutar
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        # Verificar
        self.assertTrue(campo.get_property("validationMessage"))
        self.assertEqual(urlparse(self.driver.current_url).path, "/")

    def test_08_seleccion_de_perfil(self):
        # Inicializar
        usuario = "multi_prueba"
        # Ejecutar
        self.ingresar(usuario, CLAVE)
        # Verificar
        self.espera.until(EC.url_contains("/elegir-rol"))
        self.assertEqual(self.driver.find_element(By.TAG_NAME, "h1").text, "Selecciona tu perfil")
        self.assertTrue(self.driver.find_element(By.LINK_TEXT, "Coordinador").is_displayed())
        self.assertTrue(self.driver.find_element(By.LINK_TEXT, "Docente").is_displayed())

    def test_09_cierre_de_sesion(self):
        # Inicializar
        self.ingresar("coordinador_prueba", CLAVE)
        self.espera.until(EC.url_contains("/coordinador"))
        # Ejecutar
        self.driver.find_element(By.CSS_SELECTOR, ".salir-btn").click()
        self.espera.until(EC.title_is("Iniciar sesión"))
        self.driver.get(self.aplicacion.url + "/coordinador")
        # Verificar
        self.espera.until(EC.title_is("Iniciar sesión"))
        self.assertEqual(urlparse(self.driver.current_url).path, "/")

    def test_10_panel_sin_sesion(self):
        # Inicializar
        direccion = self.aplicacion.url + "/coordinador"
        # Ejecutar
        self.driver.get(direccion)
        # Verificar
        self.espera.until(EC.title_is("Iniciar sesión"))
        self.assertEqual(urlparse(self.driver.current_url).path, "/")

    def test_11_coordinador_no_es_director(self):
        # Inicializar
        self.ingresar("coordinador_prueba", CLAVE)
        self.espera.until(EC.url_contains("/coordinador"))
        # Ejecutar
        self.driver.get(self.aplicacion.url + "/director")
        # Verificar
        self.assertIn("Forbidden", self.driver.find_element(By.TAG_NAME, "h1").text)


if __name__ == "__main__":
    unittest.main(verbosity=2)

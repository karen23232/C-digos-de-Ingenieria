import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class TestLogin(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://violet-wolf-820033.hostingersite.com/iniciodesesion.php")

    def test_login_campos_vacios(self):
        # Intenta enviar el formulario sin llenar los campos
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(1)

        # Verifica que aún esté en la página de inicio de sesión
        current_url = self.driver.current_url
        self.assertIn("iniciodesesion.php", current_url, "El formulario se envió a pesar de tener campos vacíos.")

    def test_login_usuario_incorrecto(self):
        self.driver.find_element(By.ID, "correoUsuario").send_keys("lini@gmail.com")
        self.driver.find_element(By.ID, "contraseniaUsuario").send_keys("libia")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)
        self.assertIn("Usuario incorrecto", self.driver.page_source)

    def test_login_contrasena_incorrecta(self):
        self.driver.find_element(By.ID, "correoUsuario").send_keys("libia@gmail.com")
        self.driver.find_element(By.ID, "contraseniaUsuario").send_keys("contrasena_incorrecta")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)
        self.assertIn("Contraseña incorrecta", self.driver.page_source)

    def test_login_correcto(self):
        self.driver.find_element(By.ID, "correoUsuario").send_keys("libia@gmail.com")
        self.driver.find_element(By.ID, "contraseniaUsuario").send_keys("libia")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)
        self.assertIn("paginaprincipal", self.driver.current_url)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()

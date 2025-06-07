import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class PruebaSeguridadRegistro(unittest.TestCase):
    def setUp(self):
        # Configurar el driver antes de cada prueba
        self.driver = webdriver.Chrome()
        self.url = "URL_DE_TU_FORMULARIO"
        self.driver.get(self.url)
        time.sleep(2)

    def registrar_usuario(self, nombre, correo, contrasenia):
        driver = self.driver

        driver.find_element(By.ID, "nombreUsuario").clear()
        driver.find_element(By.ID, "nombreUsuario").send_keys(nombre)

        driver.find_element(By.ID, "correoUsuario").clear()
        driver.find_element(By.ID, "correoUsuario").send_keys(correo)

        driver.find_element(By.ID, "contraseniaUsuario").clear()
        driver.find_element(By.ID, "contraseniaUsuario").send_keys(contrasenia)

        driver.find_element(By.CSS_SELECTOR, ".btn.btn-custom").click()
        time.sleep(2)

        return driver.page_source

    def test_seguridad_inyeccion_sql(self):
        payloads = [
            ("' OR '1'='1", "ataque@gmail.com", "1234"),
            ("admin' --", "admin@gmail.com", "1234"),
            ("1; DROP TABLE usuarios", "drop@gmail.com", "1234")
        ]

        for nombre, correo, contrasenia in payloads:
            with self.subTest(payload=nombre):
                print(f"\n➡️ Probando Inyección SQL con nombre: {nombre}")
                mensaje = self.registrar_usuario(nombre, correo, contrasenia)
                if "error" in mensaje.lower() or "exception" in mensaje.lower():
                    print("❌ Vulnerabilidad detectada (mensaje de error visible)")
                else:
                    print("✅ No se evidenció vulnerabilidad aparente")

                self.driver.get(self.url)
                time.sleep(1)

    def test_seguridad_xss(self):
        payloads = [
            ("<script>alert('XSS')</script>", "xss@gmail.com", "1234"),
            ("<img src='x' onerror='alert(1)'>", "imagen@gmail.com", "1234")
        ]

        for nombre, correo, contrasenia in payloads:
            with self.subTest(payload=nombre):
                print(f"\n➡️ Probando XSS con nombre: {nombre}")
                mensaje = self.registrar_usuario(nombre, correo, contrasenia)
                if "<script>" in mensaje.lower() or "alert(" in mensaje.lower():
                    print("❌ Posible vulnerabilidad XSS detectada")
                else:
                    print("✅ No se evidenció vulnerabilidad aparente")

                self.driver.get(self.url)
                time.sleep(1)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()

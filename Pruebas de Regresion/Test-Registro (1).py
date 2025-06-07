import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class PruebaRegresionRegistro(unittest.TestCase):
    def setUp(self):
        # Configurar el driver antes de cada prueba
        self.driver = webdriver.Chrome()
        self.url = "URL_DE_TU_FORMULARIO"
        self.driver.get(self.url)
        time.sleep(2)

    def registrar_usuario(self, nombre, correo, contrasenia):
        driver = self.driver

        # Localizar y llenar los campos
        driver.find_element(By.ID, "nombreUsuario").clear()
        driver.find_element(By.ID, "nombreUsuario").send_keys(nombre)

        driver.find_element(By.ID, "correoUsuario").clear()
        driver.find_element(By.ID, "correoUsuario").send_keys(correo)

        driver.find_element(By.ID, "contraseniaUsuario").clear()
        driver.find_element(By.ID, "contraseniaUsuario").send_keys(contrasenia)

        # Click en botón de registro
        driver.find_element(By.CSS_SELECTOR, ".btn.btn-custom").click()
        time.sleep(3)

        # Devolver el contenido de la página
        return driver.page_source

    def test_casos_regresion(self):
        # Lista de casos de prueba
        casos_prueba = [
            ("lucia", "lucia@gmail.com", "1234", "CP018"),
            ("lucia", "otrocorreo@gmail.com", "1234", "CP019"),
            ("otro", "lucia@gmail.com", "1234", "CP020"),
            ("lucia", "lucia@gmail.com", "1234", "CP021"),
            ("pepe", "", "1234", "CP022"),
            ("pepe", "pepe@gmail.com", "", "CP023"),
            ("", "pepe@gmail.com", "1234", "CP024")
        ]

        for nombre, correo, contrasenia, caso in casos_prueba:
            with self.subTest(caso=caso):
                print(f"\n➡️ Ejecutando {caso}...")
                mensaje = self.registrar_usuario(nombre, correo, contrasenia)

                if "Registro exitoso" in mensaje:
                    print(f"✅ {caso}: Registro exitoso")
                elif "ya está en uso" in mensaje:
                    print(f"⚠️ {caso}: Usuario o correo ya registrado")
                elif "Debe completar el campo" in mensaje or "obligatorio" in mensaje:
                    print(f"❌ {caso}: Faltan campos obligatorios")
                else:
                    print(f"❌ {caso}: Resultado inesperado")

                # Refrescar la página para el siguiente caso
                self.driver.get(self.url)
                time.sleep(2)

    def tearDown(self):
        # Cerrar navegador después de cada prueba
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()

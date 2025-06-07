import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class PruebaPreferenciaNotificaciones(unittest.TestCase):
    def setUp(self):
        # Configurar el driver
        self.driver = webdriver.Chrome()
        self.url = "URL_DE_TU_FORMULARIO"
        self.driver.get(self.url)
        time.sleep(2)

    def configurar_preferencias(self, recibir_notif, tipo_notif):
        driver = self.driver

        # Localizar y marcar/desmarcar checkbox de notificaciones
        checkbox = driver.find_element(By.ID, "recibirNotificaciones")
        if checkbox.is_selected() != recibir_notif:
            checkbox.click()

        # Seleccionar tipo de notificación si está habilitado
        if recibir_notif:
            select = driver.find_element(By.ID, "tipoNotificacion")
            opciones = select.find_elements(By.TAG_NAME, "option")
            for opcion in opciones:
                if opcion.text == tipo_notif:
                    opcion.click()
                    break

        # Guardar preferencias
        driver.find_element(By.CSS_SELECTOR, ".btn.btn-guardar").click()
        time.sleep(2)

        # Retornar el contenido de la página tras guardar
        return driver.page_source

    def test_preferencias_notificaciones(self):
        casos_prueba = [
            (True, "Correo electrónico"),
            (True, "SMS"),
            (True, "Notificación push"),
            (False, "")  # Sin seleccionar tipo si no se desea recibir notificaciones
        ]

        for recibir, tipo in casos_prueba:
            with self.subTest(preferencia=(recibir, tipo)):
                print(f"\n➡️ Configurando notificaciones: recibir={recibir}, tipo='{tipo}'")
                mensaje = self.configurar_preferencias(recibir, tipo)
                if "Preferencias actualizadas" in mensaje:
                    print("✅ Preferencia registrada correctamente")
                elif "Debe seleccionar un tipo de notificación" in mensaje and recibir:
                    print("⚠️ Faltó seleccionar tipo de notificación")
                else:
                    print("❌ Resultado inesperado o error en la configuración")

                self.driver.get(self.url)
                time.sleep(2)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()

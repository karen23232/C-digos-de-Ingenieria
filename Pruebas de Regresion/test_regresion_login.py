from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import time

# Ruta del driver
RUTA_DRIVER = os.path.join(os.getcwd(), "chromedriver.exe")

# Configuración del navegador
service = Service(RUTA_DRIVER)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# Maximiza la ventana
driver.maximize_window()

# URL del módulo de inicio de sesión
URL_LOGIN = "http://violet-wolf-820033.hostingersite.com/iniciodesesion.php"

# Credenciales válidas para la prueba
USUARIO = "karen@gmail.com"
CONTRASENA = "karen"

def esperar(segundos=2):
    time.sleep(segundos)

def prueba_inicio_sesion_exitosa():
    print("🔍 Iniciando prueba de regresión para el login...")

    driver.get(URL_LOGIN)
    esperar()

    # Buscar los campos de correo y contraseña
    campo_correo = driver.find_element(By.ID, "correoUsuario")
    campo_contrasena = driver.find_element(By.ID, "contraseniaUsuario")

    campo_correo.clear()
    campo_contrasena.clear()

    campo_correo.send_keys(USUARIO)
    campo_contrasena.send_keys(CONTRASENA)

    # Enviar el formulario
    campo_contrasena.send_keys(Keys.ENTER)

    esperar(3)

    # Verificar si el inicio fue exitoso
    if "error" in driver.current_url:
        print("❌ Falló la prueba de regresión: redirigió con error.")
    else:
        print("✅ Prueba de regresión superada: inició sesión correctamente.")

def finalizar():
    print("🧹 Cerrando navegador.")
    driver.quit()

if __name__ == "__main__":
    prueba_inicio_sesion_exitosa()
    finalizar()

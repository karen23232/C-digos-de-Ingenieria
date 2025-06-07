from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
import time

# Configuración de entorno
RUTA_DRIVER = os.path.join(os.getcwd(), "chromedriver.exe")
service = Service(RUTA_DRIVER)
driver = webdriver.Chrome(service=service)
driver.maximize_window()

# Credenciales y enlaces
USUARIO = "karen@gmail.com"
CONTRASENA = "karen"
URL_LOGIN = "http://violet-wolf-820033.hostingersite.com/iniciodesesion.php"
URL_PRINCIPAL = "http://violet-wolf-820033.hostingersite.com/FrontEnd/paginaprincipal.html"
URL_CONSULTA = "http://violet-wolf-820033.hostingersite.com/BackEnd/mostrarvehiculos.php"

def esperar(segundos=2):
    time.sleep(segundos)

def iniciar_sesion():
    print("🔐 Iniciando sesión...")

    driver.get(URL_LOGIN)
    esperar()

    correo = driver.find_element(By.ID, "correoUsuario")
    clave = driver.find_element(By.ID, "contraseniaUsuario")

    correo.clear()
    clave.clear()
    correo.send_keys(USUARIO)
    clave.send_keys(CONTRASENA)

    # Click en el botón Iniciar Sesión
    driver.find_element(By.XPATH, "//button[contains(text(),'Iniciar Sesión')]").click()
    esperar(3)

    if "error" in driver.current_url:
        print("❌ Falló el inicio de sesión.")
        return False
    print("✅ Inicio de sesión exitoso.")
    return True

def consultar_vehiculos():
    print("🚗 Accediendo a consulta de vehículos...")

    driver.get(URL_PRINCIPAL)
    esperar(2)

    # Buscar enlace al módulo mostrarvehiculos.php y hacer clic
    try:
        boton_consultar = driver.find_element(By.XPATH, "//a[contains(@href, 'mostrarvehiculos.php')]")
        boton_consultar.click()
    except:
        print("❌ No se encontró el botón/enlace que lleva a 'mostrarvehiculos.php'.")
        return False

    esperar(3)

    # Verificar si se llegó correctamente a la página
    if URL_CONSULTA not in driver.current_url:
        print("❌ No se redireccionó correctamente a la página de consulta.")
        return False

    # Verificar que la tabla tenga filas de vehículos
    try:
        filas = driver.find_elements(By.XPATH, "//table//tr")
        if len(filas) > 1:
            print(f"✅ Consulta exitosa: se encontraron {len(filas)-1} vehículo(s).")
            return True
        else:
            print("⚠️ Página cargó pero no hay vehículos registrados.")
            return True
    except:
        print("❌ Error al verificar los vehículos.")
        return False

def finalizar():
    print("🧹 Cerrando navegador.")
    driver.quit()

# Flujo completo de prueba
if __name__ == "__main__":
    if iniciar_sesion():
        consultar_vehiculos()
    finalizar()

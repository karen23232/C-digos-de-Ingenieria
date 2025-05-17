from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import os

# Configurar navegador
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Crear carpeta para capturas
os.makedirs("capturas", exist_ok=True)

def capturar(nombre_archivo):
    ruta = f"capturas/{nombre_archivo}.png"
    driver.save_screenshot(ruta)
    print(f"📸 Captura guardada: {ruta}")

try:
    # 1. Acceder a la página de login
    driver.get("https://violet-wolf-820033.hostingersite.com/iniciodesesion.php")
    time.sleep(2)
    capturar("01_login_cargado")

    # 2. Ingresar credenciales
    driver.find_element(By.ID, "correoUsuario").send_keys("juan@gmail.com")
    driver.find_element(By.ID, "contraseniaUsuario").send_keys("J")
    capturar("02_login_datos_ingresados")

    # 3. Clic en botón "Iniciar Sesión"
    driver.find_element(By.CSS_SELECTOR, "button.btn-custom").click()
    time.sleep(3)
    capturar("03_login_exitoso")

    # 4. Verificar que se cargó la página principal (opcional, según tu lógica)
    print("📄 Título actual:", driver.title)

    # 5. Hacer clic en "Consultar Vehículos"
    driver.find_element(By.CSS_SELECTOR, "a[href*='mostrarvehiculos.php']").click()
    time.sleep(3)
    capturar("04_pagina_vehiculos_cargada")

    # 6. Verificar presencia de tabla con vehículos
    tabla = driver.find_element(By.TAG_NAME, "table")
    print("✅ Tabla de vehículos encontrada.")
    capturar("05_tabla_visible")

    # 7. Verificar filas de datos en la tabla (más de una = hay datos además del encabezado)
    filas = tabla.find_elements(By.TAG_NAME, "tr")
    if len(filas) > 1:
        print(f"✅ Se encontraron {len(filas) - 1} vehículos registrados.")
        capturar("06_vehiculos_registrados")
    else:
        print("⚠️ No hay vehículos registrados.")
        capturar("06_sin_vehiculos")

except Exception as e:
    print(f"⚠️ Error durante la prueba: {e}")
    capturar("error_consulta_vehiculos")

finally:
    time.sleep(2)
    driver.quit()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
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
    wait = WebDriverWait(driver, 10)

    # 1. Acceder al login
    driver.get("https://violet-wolf-820033.hostingersite.com/iniciodesesion.php")
    time.sleep(2)
    capturar("01_login_cargado")

    # 2. Llenar formulario de login
    driver.find_element(By.ID, "correoUsuario").send_keys("juan@gmail.com")
    driver.find_element(By.ID, "contraseniaUsuario").send_keys("J")
    capturar("02_login_datos_ingresados")

    # 3. Iniciar sesión
    driver.find_element(By.CSS_SELECTOR, "button.btn-custom").click()
    time.sleep(3)
    capturar("03_login_exitoso")

    # 4. Ir a la página de Pico y Placa
    driver.get("https://violet-wolf-820033.hostingersite.com/FrontEnd/consultarpp.php")
    time.sleep(3)
    capturar("04_pagina_pico_placa")

    # 5. Seleccionar un vehículo (radio button)
    radio = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='radio']")))
    radio.click()
    time.sleep(1)

    # 6. Ingresar una fecha válida
    campo_fecha = driver.find_element(By.CSS_SELECTOR, "input[type='date']")
    campo_fecha.send_keys("03052025")
    time.sleep(1)
    capturar("05_datos_ingresados")

    # 7. Hacer clic en "Consultar Pico y Placa"
    boton = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//form[@id='formulario']//button[@type='submit' and contains(., 'Consultar Pico y Placa')]")
    ))
    boton.click()
    time.sleep(3)
    capturar("06_resultado_consulta")

    print("✅ Consulta de Pico y Placa ejecutada correctamente.")

except Exception as e:
    print(f"❌ Error en la prueba: {e}")
    capturar("error_general")

finally:
    time.sleep(2)
    driver.quit()

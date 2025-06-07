from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# Configuración del navegador
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
os.makedirs("capturas_seguridad", exist_ok=True)

def capturar(nombre):
    driver.save_screenshot(f"capturas_seguridad/{nombre}.png")

try:
    # 1️⃣ INICIAR SESIÓN
    driver.get("https://violet-wolf-820033.hostingersite.com/iniciodesesion.php")
    time.sleep(2)
    driver.find_element(By.NAME, "correoUsuario").send_keys("juan@gmail.com")
    driver.find_element(By.NAME, "contraseniaUsuario").send_keys("J")
    driver.find_element(By.XPATH, "//button[contains(text(),'Iniciar Sesión')]").click()
    time.sleep(3)
    capturar("01_sesion_iniciada")
    print("✅ Sesión iniciada correctamente.")

    # 2️⃣ ACCEDER AL MÓDULO DE PICO Y PLACA
    driver.get("https://violet-wolf-820033.hostingersite.com/FrontEnd/consultarpp.php")
    time.sleep(3)
    capturar("02_modulo_pico_placa")
    print("✅ Módulo de Pico y Placa cargado.")

    wait = WebDriverWait(driver, 10)

    # 3️⃣ SELECCIONAR VEHÍCULO (primero que aparezca)
    radios = driver.find_elements(By.NAME, "vehiculoSeleccionado")
    if not radios:
        raise Exception("❌ No se encontró ningún vehículo para seleccionar.")
    radios[0].click()
    print("✅ Vehículo seleccionado.")

    # 🔍 Función para hacer clic de forma robusta
    def click_consultar():
        boton = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.logout-button")))
        boton.click()

    # 4️⃣ PRUEBA DE SQL INJECTION
    driver.find_element(By.ID, "fecha").clear()
    driver.find_element(By.ID, "fecha").send_keys("2025-05-05' OR '1'='1")
    click_consultar()
    time.sleep(2)
    capturar("03_sql_injection")
    print("🧨 Prueba de SQL Injection ejecutada. Verifica si hubo errores o datos alterados.")

    # 5️⃣ PRUEBA DE XSS
    driver.find_element(By.ID, "fecha").clear()
    driver.find_element(By.ID, "fecha").send_keys("<script>alert('XSS')</script>")
    click_consultar()
    time.sleep(2)
    capturar("04_xss")
    print("🧬 Prueba de XSS ejecutada. Observa si aparece un pop-up o algo raro en pantalla.")

    # 6️⃣ PRUEBA DE CSRF (simulada con recarga sin token)
    driver.refresh()
    time.sleep(2)
    radios = driver.find_elements(By.NAME, "vehiculoSeleccionado")
    radios[0].click()
    driver.find_element(By.ID, "fecha").clear()
    driver.find_element(By.ID, "fecha").send_keys("2025-05-05")
    click_consultar()
    time.sleep(2)
    capturar("05_csrf")
    print("🔓 Prueba de CSRF ejecutada (nota: tu código no usa token CSRF).")

except Exception as e:
    print(f"⚠️ Error en la prueba: {e}")
    capturar("error_seguridad")

finally:
    time.sleep(2)
    driver.quit()
    print("🚦 Pruebas finalizadas.")

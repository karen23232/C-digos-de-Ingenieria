from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# Configuración del navegador
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Carpeta para capturas
os.makedirs("capturas", exist_ok=True)
def capturar(nombre):
    ruta = f"capturas/{nombre}.png"
    driver.save_screenshot(ruta)
    # print(f"📸 Captura: {ruta}")  # Comentado para evitar mostrar en consola

try:
    # 1. Iniciar sesión
    driver.get("https://violet-wolf-820033.hostingersite.com/iniciodesesion.php")
    time.sleep(2)
    driver.find_element(By.NAME, "correoUsuario").send_keys("juan@gmail.com")
    driver.find_element(By.NAME, "contraseniaUsuario").send_keys("J")
    driver.find_element(By.XPATH, "//button[contains(text(),'Iniciar Sesión')]").click()
    time.sleep(3)
    capturar("01_sesion_iniciada")

    # 2. Ir a "Consultar Pico y Placa"
    driver.get("https://violet-wolf-820033.hostingersite.com/FrontEnd/consultarpp.php")
    time.sleep(3)
    capturar("02_pagina_pico_y_placa")

    # 3. Seleccionar un vehículo
    vehiculos = driver.find_elements(By.NAME, "vehiculoSeleccionado")
    if not vehiculos:
        print("❌ No hay vehículos disponibles para seleccionar.")
        capturar("03_sin_vehiculos")
        raise Exception("No se puede continuar sin vehículos.")
    vehiculos[0].click()  # Selecciona el primero
    print("✅ Vehículo seleccionado.")
    capturar("03_vehiculo_seleccionado")

    # 4. Seleccionar una fecha
    fecha_input = driver.find_element(By.ID, "fecha")
    fecha_input.send_keys("18-05-2025")  # Cambia la fecha para probar distintos escenarios
    print("📅 Fecha seleccionada: 18-05-2025")
    capturar("04_fecha_seleccionada")

    # 5. Scroll y clic en botón "Consultar Pico y Placa"
    boton = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary[type='submit']")
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", boton)
    time.sleep(1)
    boton.click()
    time.sleep(3)
    capturar("05_resultado_mostrado")

    # 6. Verificar resultado
    resultado = driver.find_element(By.ID, "resultado-container").text
    print(f"📋 Resultado mostrado:\n{resultado}")

    if "No puedes circular" in resultado or "Puedes circular" in resultado:
        print("✅ Resultado de Pico y Placa mostrado correctamente.")
    else:
        print("❌ El resultado no contiene el mensaje esperado.")

except Exception as e:
    print(f"⚠️ Error en la prueba: {e}")
    capturar("error_general")

finally:
    time.sleep(2)
    driver.quit()

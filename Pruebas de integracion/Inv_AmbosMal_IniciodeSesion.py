
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Configuración del WebDriver
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # 1. Ir al login
    driver.get("https://violet-wolf-820033.hostingersite.com/iniciodesesion.php")
    time.sleep(2)
    driver.save_screenshot("01_pagina_login.png")

    # 2. Ingresar correo y contraseña incorrectos
    email_input = driver.find_element(By.NAME, "correoUsuario")
    password_input = driver.find_element(By.NAME, "contraseniaUsuario")

    email_input.send_keys("noexiste@email.com")
    password_input.send_keys("claveIncorrecta")
    driver.save_screenshot("02_datos_ingresados.png")

    # 3. Enviar el formulario
    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_button.click()
    time.sleep(3)
    driver.save_screenshot("03_despues_click_login.png")

    # 4. Verificar si aparece el mensaje de error correspondiente
    page_source = driver.page_source
    if "⚠️ Usuario incorrecto. Intenta de nuevo." in page_source:
        print("✅ Mensaje de error por usuario no registrado detectado correctamente.")
        driver.save_screenshot("04_mensaje_error_detectado.png")
    else:
        print("❌ No se detectó el mensaje esperado para usuario incorrecto.")
        driver.save_screenshot("04_mensaje_error_no_detectado.png")

finally:
    driver.quit()

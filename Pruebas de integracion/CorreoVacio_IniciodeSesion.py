
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

# Configuración del WebDriver
options = Options()
options.add_argument("--start-maximized")
service = Service()
driver = webdriver.Chrome(service=service, options=options)

try:
    # 1. Abrir la página de inicio de sesión
    driver.get("https://violet-wolf-820033.hostingersite.com/iniciodesesion.php")
    time.sleep(1)
    driver.save_screenshot("01_pagina_login.png")

    # 2. Localizar campos
    correo_input = driver.find_element(By.NAME, "correoUsuario")
    contrasenia_input = driver.find_element(By.NAME, "contraseniaUsuario")

    # 3. Dejar vacío el correo y llenar solo la contraseña
    correo_input.clear()
    contrasenia_input.send_keys("123")
    driver.save_screenshot("02_solo_contrasena_ingresada.png")

    # 4. Intentar enviar el formulario
    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_button.click()
    time.sleep(1)
    driver.save_screenshot("03_despues_click_enviar.png")

    # 5. Verificar si la página se quedó en el mismo lugar (no redirigió)
    if driver.current_url == "https://violet-wolf-820033.hostingersite.com/iniciodesesion.php":
        print("✅ Campo 'correo' vacío: el navegador bloqueó el envío con 'Completa este campo'.")
        driver.save_screenshot("04_envio_bloqueado.png")
    else:
        print("❌ El formulario se envió a pesar de que el campo 'correo' estaba vacío.")
        driver.save_screenshot("04_envio_incorrecto.png")

finally:
    driver.quit()

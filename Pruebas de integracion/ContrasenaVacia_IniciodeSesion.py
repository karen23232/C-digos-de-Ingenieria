
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

    # 3. Ingresar correo válido, pero dejar contraseña vacía
    correo_input.send_keys("jack@gmail.com")
    contrasenia_input.clear()
    driver.save_screenshot("02_solo_correo_ingresado.png")

    # 4. Intentar enviar el formulario
    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_button.click()
    time.sleep(1)
    driver.save_screenshot("03_despues_click_enviar.png")

    # 5. Verificar si el formulario no se envió (misma URL)
    if driver.current_url == "https://violet-wolf-820033.hostingersite.com/iniciodesesion.php":
        print("✅ Campo 'contraseña' vacío: el navegador bloqueó el envío con 'Completa este campo'.")
        driver.save_screenshot("04_envio_bloqueado.png")
    else:
        print("❌ El formulario se envió a pesar de que la contraseña estaba vacía.")
        driver.save_screenshot("04_envio_incorrecto.png")

finally:
    driver.quit()

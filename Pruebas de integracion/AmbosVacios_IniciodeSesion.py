
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
    # 1. Ir a la página de inicio de sesión
    driver.get("https://violet-wolf-820033.hostingersite.com/iniciodesesion.php")
    time.sleep(1)
    driver.save_screenshot("01_pagina_login.png")

    # 2. Localizar los elementos
    correo_input = driver.find_element(By.NAME, "correoUsuario")
    contrasenia_input = driver.find_element(By.NAME, "contraseniaUsuario")
    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")

    # 3. Dejar vacío solo el campo de correo
    correo_input.clear()
    contrasenia_input.send_keys("123")

    # 4. Intentar enviar el formulario (correo vacío)
    submit_button.click()
    time.sleep(1)
    driver.save_screenshot("02_envio_sin_correo.png")

    if driver.current_url == "https://violet-wolf-820033.hostingersite.com/iniciodesesion.php":
        print("✅ Campo 'correo' vacío: el navegador bloqueó el envío con 'Completa este campo'.")

        # 5. Ahora llenar solo el correo y dejar contraseña vacía
        correo_input.send_keys("jack@gmail.com")
        contrasenia_input.clear()

        # 6. Intentar enviar nuevamente (contraseña vacía)
        submit_button.click()
        time.sleep(1)
        driver.save_screenshot("03_envio_sin_contrasena.png")

        if driver.current_url == "https://violet-wolf-820033.hostingersite.com/iniciodesesion.php":
            print("✅ Campo 'contraseña' vacío: el navegador bloqueó el envío con 'Completa este campo'.")
            print("✅ Prueba de validación individual de campos vacíos pasada.")
        else:
            print("❌ El formulario se envió a pesar de que la contraseña estaba vacía.")
    else:
        print("❌ El formulario se envió a pesar de que el correo estaba vacío.")

finally:
    driver.save_screenshot("04_estado_final.png")
    driver.quit()

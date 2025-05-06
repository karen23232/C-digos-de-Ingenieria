
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Configura la URL de login
URL_LOGIN = "https://violet-wolf-820033.hostingersite.com/iniciodesesion.php"

# Inicia el navegador
driver = webdriver.Chrome()

try:
    driver.get(URL_LOGIN)
    time.sleep(2)
    driver.save_screenshot("01_pagina_login.png")

    # Localiza e ingresa el correo incorrecto y contraseña válida
    correo_input = driver.find_element(By.NAME, "correoUsuario")
    contrasena_input = driver.find_element(By.NAME, "contraseniaUsuario")

    correo_input.send_keys("usuariofalso@email.com")  # correo incorrecto
    contrasena_input.send_keys("123")  # contraseña válida
    driver.save_screenshot("02_datos_ingresados.png")

    # Clic en el botón de iniciar sesión
    driver.find_element(By.XPATH, "//button[text()='Iniciar Sesión']").click()
    time.sleep(3)
    driver.save_screenshot("03_despues_click_login.png")

    # Revisa si aparece el mensaje de error
    body_text = driver.find_element(By.TAG_NAME, "body").text
    if "Usuario incorrecto" in body_text:
        print("✅ Prueba exitosa: Mensaje de error mostrado correctamente.")
        driver.save_screenshot("04_mensaje_error.png")
    else:
        print("❌ Prueba fallida: No se mostró el mensaje de error esperado.")
        driver.save_screenshot("04_sin_mensaje_error.png")

finally:
    driver.quit()


from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# URL del login
URL_LOGIN = "https://violet-wolf-820033.hostingersite.com/iniciodesesion.php"

# Datos del usuario
correo_valido = "jack@gmail.com"
contrasena_invalida = "contraseña_incorrecta"

# Inicia el navegador
driver = webdriver.Chrome()

try:
    driver.get(URL_LOGIN)
    time.sleep(2)
    driver.save_screenshot("01_pagina_login.png")

    # Ingresa correo válido y contraseña incorrecta
    correo_input = driver.find_element(By.NAME, "correoUsuario")
    contrasena_input = driver.find_element(By.NAME, "contraseniaUsuario")

    correo_input.send_keys(correo_valido)
    contrasena_input.send_keys(contrasena_invalida)
    driver.save_screenshot("02_datos_ingresados.png")

    # Clic en botón "Iniciar Sesión"
    driver.find_element(By.XPATH, "//button[text()='Iniciar Sesión']").click()
    time.sleep(3)
    driver.save_screenshot("03_despues_click_login.png")

    # Verifica que no hubo redirección a la página principal
    if driver.current_url == "https://violet-wolf-820033.hostingersite.com/FrontEnd/paginaprincipal.html":
        print("❌ Prueba fallida: Redireccionó a la página principal con contraseña incorrecta.")
        driver.save_screenshot("04_redireccion_incorrecta.png")
    else:
        # Verifica si aparece mensaje de error esperado
        body_text = driver.find_element(By.TAG_NAME, "body").text
        if "Contraseña incorrecta" in body_text:
            print("✅ Prueba exitosa: Mensaje de error mostrado correctamente al usar contraseña incorrecta.")
            driver.save_screenshot("04_mensaje_error.png")
        else:
            print("❌ Prueba fallida: No se mostró el mensaje esperado de 'Contraseña incorrecta'.")
            driver.save_screenshot("04_sin_mensaje_error.png")
finally:
    driver.quit()

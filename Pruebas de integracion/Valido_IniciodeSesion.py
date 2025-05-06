
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

URL_LOGIN = "https://violet-wolf-820033.hostingersite.com/iniciodesesion.php"
URL_ESPERADA_EXITO = "https://violet-wolf-820033.hostingersite.com/FrontEnd/paginaprincipal.html"

# Credenciales válidas de prueba
correo = "jack@gmail.com"
contrasena = "123"

# Iniciar navegador
driver = webdriver.Chrome()

try:
    driver.get(URL_LOGIN)
    time.sleep(2)
    driver.save_screenshot("01_pagina_login.png")

    # Ingresar correo
    correo_input = driver.find_element(By.NAME, "correoUsuario")
    correo_input.send_keys(correo)

    # Ingresar contraseña
    pass_input = driver.find_element(By.NAME, "contraseniaUsuario")
    pass_input.send_keys(contrasena)

    driver.save_screenshot("02_credenciales_ingresadas.png")

    # Clic en botón de iniciar sesión
    boton = driver.find_element(By.XPATH, "//button[text()='Iniciar Sesión']")
    boton.click()

    # Esperar redirección o mensaje
    time.sleep(3)
    driver.save_screenshot("03_despues_click_login.png")

    if driver.current_url == URL_ESPERADA_EXITO:
        print("✅ Inicio de sesión exitoso. Redirección correcta.")
        driver.save_screenshot("04_exito_redireccion.png")
    else:
        try:
            mensaje_error = driver.find_element(By.XPATH, "//*[contains(text(),'Usuario incorrecto')]")
            print("⚠️ Inicio de sesión fallido. Mensaje de error mostrado correctamente.")
            driver.save_screenshot("04_mensaje_error.png")
        except:
            print(f"❌ Prueba fallida. Ni redirección ni mensaje de error detectados. URL actual: {driver.current_url}")
            driver.save_screenshot("04_fallo_sin_mensaje.png")

finally:
    driver.quit()

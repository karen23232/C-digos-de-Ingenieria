from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def realizar_registro_usuario(nombre, correo, contrasena):
    # Configurar Chrome con WebDriver Manager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()

    try:
        # 1. Acceder a la página de registro de usuario
        print("Accediendo a la página de registro de usuario...")
        driver.get("https://violet-wolf-820033.hostingersite.com/registro.html")
        driver.save_screenshot("registro_usuario_pagina_inicial.png")
        print("Página de registro de usuario cargada.")

        # 2. Completar los campos del formulario
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "nombreUsuario"))
        )
        driver.find_element(By.ID, "nombreUsuario").send_keys(nombre)
        driver.find_element(By.ID, "correoUsuario").send_keys(correo)
        driver.find_element(By.ID, "contraseniaUsuario").send_keys(contrasena)

        print(f"Datos ingresados: Nombre={nombre}, Correo={correo}, Contraseña={contrasena}")

        # 3. Hacer clic en el botón 'Registrarse'
        registrar_button = driver.find_element(By.CSS_SELECTOR, "button.btn-custom")
        registrar_button.click()
        print("Botón de 'Registrarse' presionado.")

        # 4. Esperar un momento para que se procese el registro
        time.sleep(3)  # Aquí puedes ajustar dependiendo de la respuesta de la web

        # 5. Capturar pantalla del resultado
        driver.save_screenshot("registro_usuario_resultado.png")
        print("Registro completado. Captura tomada.")

    finally:
        driver.quit()
        print("Prueba de registro de usuario finalizada.")

# Datos de prueba
realizar_registro_usuario(
    nombre="Sebas Tester",
    correo="sebas.tester@example.com",
    contrasena="Clave123"
)

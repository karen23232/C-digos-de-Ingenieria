from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import time

URL = "https://violet-wolf-820033.hostingersite.com/registro.html"

def iniciar_driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    return driver

def enviar_formulario(driver, nombre, correo, contrasenia):
    driver.get(URL)
    time.sleep(1)
    driver.find_element(By.NAME, "nombreUsuario").clear()
    driver.find_element(By.NAME, "nombreUsuario").send_keys(nombre)
    driver.find_element(By.NAME, "correoUsuario").clear()
    driver.find_element(By.NAME, "correoUsuario").send_keys(correo)
    driver.find_element(By.NAME, "contraseniaUsuario").clear()
    driver.find_element(By.NAME, "contraseniaUsuario").send_keys(contrasenia)
    driver.find_element(By.XPATH, "//button[contains(text(),'Registrarse')]").click()
    time.sleep(3)

def obtener_mensaje(driver):
    try:
        mensaje_div = driver.find_element(By.CLASS_NAME, "mensaje")
        return mensaje_div.text.strip()
    except NoSuchElementException:
        return None

def probar_registro_exitoso():
    driver = iniciar_driver()
    enviar_formulario(driver, "usuarioPrueba123", "usuarioPrueba123@example.com", "Contrasenia123!")
    mensaje = obtener_mensaje(driver)
    assert "Registro exitoso" in mensaje, f"Esperaba éxito pero obtuve: {mensaje}"
    print("✅ Registro exitoso OK")
    driver.quit()

def probar_usuario_duplicado():
    driver = iniciar_driver()
    # Usamos el mismo usuario/correo para simular duplicado
    enviar_formulario(driver, "usuarioPrueba123", "usuarioPrueba123@example.com", "Contrasenia123!")
    mensaje = obtener_mensaje(driver)
    assert "correo y el usuario ya están en uso" in mensaje, f"Esperaba error de duplicado pero obtuve: {mensaje}"
    print("✅ Detección de usuario duplicado OK")
    driver.quit()

def probar_campos_vacios():
    driver = iniciar_driver()
    driver.get(URL)
    # Intentar enviar sin completar nada
    driver.find_element(By.XPATH, "//button[contains(text(),'Registrarse')]").click()
    time.sleep(1)
    # HTML5 bloquea el submit, así que detectamos si se resalta el primer input vacío
    nombre = driver.find_element(By.NAME, "nombreUsuario")
    assert nombre.get_attribute("validationMessage") != "", "Esperaba mensaje de validación en nombre"
    print("✅ Validación de campos vacíos OK")
    driver.quit()

def probar_email_invalido():
    driver = iniciar_driver()
    enviar_formulario(driver, "usuarioEmailMal", "correo-invalido", "Contrasenia123!")
    mensaje = obtener_mensaje(driver)
    # Como la validación es del frontend, probablemente no se envía el formulario
    # O el navegador puede mostrar mensaje de validación nativo, lo verificamos
    email = driver.find_element(By.NAME, "correoUsuario")
    val_msg = email.get_attribute("validationMessage")
    assert val_msg != "", "Esperaba validación de email inválido"
    print("✅ Validación de email inválido OK")
    driver.quit()

# --- Ejecutar pruebas ---
if __name__ == "__main__":
    probar_registro_exitoso()
    probar_usuario_duplicado()
    probar_campos_vacios()
    probar_email_invalido()

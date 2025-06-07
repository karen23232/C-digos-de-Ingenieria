
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

url = "https://violet-wolf-820033.hostingersite.com/iniciodesesion.php"

# Función para obtener el mensaje de alerta (si existe)
def obtener_mensaje_alerta(driver):
    try:
        alerta = driver.find_element(By.CLASS_NAME, "alert-danger")
        return alerta.text
    except:
        return None

# 1. Login exitoso
def test_login_exitoso():
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(1)
    driver.find_element(By.ID, "correoUsuario").send_keys("sofipin@gmail.com")
    driver.find_element(By.ID, "contraseniaUsuario").send_keys("123")
    driver.find_element(By.CLASS_NAME, "btn-custom").click()
    time.sleep(3)
    mensaje = obtener_mensaje_alerta(driver)
    assert mensaje is None, f"❌ Se esperaba inicio exitoso, pero apareció: {mensaje}"
    print("✅ Login exitoso: PASÓ")
    driver.quit()

# 2. Contraseña incorrecta
def test_contrasena_incorrecta():
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(1)
    driver.find_element(By.ID, "correoUsuario").send_keys("sofipin@gmail.com")
    driver.find_element(By.ID, "contraseniaUsuario").send_keys("incorrecta")
    driver.find_element(By.CLASS_NAME, "btn-custom").click()
    time.sleep(3)
    mensaje = obtener_mensaje_alerta(driver)
    assert mensaje == "⚠️ Contraseña incorrecta. Intenta de nuevo.", f"❌ Mensaje inesperado: {mensaje}"
    print("✅ Contraseña incorrecta: PASÓ")
    driver.quit()

# 3. Usuario no registrado
def test_usuario_invalido():
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(1)
    driver.find_element(By.ID, "correoUsuario").send_keys("noexiste@correo.com")
    driver.find_element(By.ID, "contraseniaUsuario").send_keys("123")
    driver.find_element(By.CLASS_NAME, "btn-custom").click()
    time.sleep(3)
    mensaje = obtener_mensaje_alerta(driver)
    assert mensaje == "⚠️ Usuario incorrecto. Intenta de nuevo.", f"❌ Mensaje inesperado: {mensaje}"
    print("✅ Usuario incorrecto: PASÓ")
    driver.quit()

# 4. Campos vacíos
def test_campos_vacios():
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(1)
    driver.find_element(By.CLASS_NAME, "btn-custom").click()
    time.sleep(2)
    # No se envía el formulario, así que alert() del navegador es lo que aparece
    print("✅ Campos vacíos: validación cliente mostrada (verificada manualmente)")
    driver.quit()

# Ejecutar todas las pruebas
if __name__ == "__main__":
    test_login_exitoso()
    test_contrasena_incorrecta()
    test_usuario_invalido()
    test_campos_vacios()

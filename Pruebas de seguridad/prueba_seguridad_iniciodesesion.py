
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# Configuración del navegador
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
os.makedirs("capturas_seguridad_login", exist_ok=True)

def capturar(nombre):
    driver.save_screenshot(f"capturas_seguridad_login/{nombre}.png")

wait = WebDriverWait(driver, 10)

try:
    # 1️⃣ LOGIN VÁLIDO
    print("✅ Prueba 1: Login válido")
    driver.get("https://violet-wolf-820033.hostingersite.com/iniciodesesion.php")
    time.sleep(2)
    driver.find_element(By.NAME, "correoUsuario").clear()
    driver.find_element(By.NAME, "correoUsuario").send_keys("sofipin@gmail.com")
    driver.find_element(By.NAME, "contraseniaUsuario").clear()
    driver.find_element(By.NAME, "contraseniaUsuario").send_keys("123")
    driver.find_element(By.XPATH, "//button[contains(text(),'Iniciar Sesión')]").click()
    time.sleep(3)
    capturar("01_login_valido")
    print("✅ Login válido probado.")

    # 2️⃣ LOGIN CON CORREO INCORRECTO
    print("⚠️ Prueba 2: Login con correo incorrecto")
    driver.get("https://violet-wolf-820033.hostingersite.com/iniciodesesion.php")
    time.sleep(2)
    driver.find_element(By.NAME, "correoUsuario").clear()
    driver.find_element(By.NAME, "correoUsuario").send_keys("noexiste@gmail.com")
    driver.find_element(By.NAME, "contraseniaUsuario").clear()
    driver.find_element(By.NAME, "contraseniaUsuario").send_keys("123")
    driver.find_element(By.XPATH, "//button[contains(text(),'Iniciar Sesión')]").click()
    time.sleep(3)
    capturar("02_login_correo_incorrecto")
    print("⚠️ Login con correo incorrecto probado.")

    # 3️⃣ LOGIN CON CONTRASEÑA INCORRECTA
    print("⚠️ Prueba 3: Login con contraseña incorrecta")
    driver.get("https://violet-wolf-820033.hostingersite.com/iniciodesesion.php")
    time.sleep(2)
    driver.find_element(By.NAME, "correoUsuario").clear()
    driver.find_element(By.NAME, "correoUsuario").send_keys("sofipin@gmail.com")
    driver.find_element(By.NAME, "contraseniaUsuario").clear()
    driver.find_element(By.NAME, "contraseniaUsuario").send_keys("000")
    driver.find_element(By.XPATH, "//button[contains(text(),'Iniciar Sesión')]").click()
    time.sleep(3)
    capturar("03_login_contrasena_incorrecta")
    print("⚠️ Login con contraseña incorrecta probado.")

    # 4️⃣ INYECCIÓN SQL SIMULADA (cookie)
    print("🧨 Prueba 4: SQL Injection en cookie")
    driver.get("https://violet-wolf-820033.hostingersite.com/iniciodesesion.php")
    time.sleep(2)
    driver.find_element(By.NAME, "correoUsuario").clear()
    driver.find_element(By.NAME, "correoUsuario").send_keys("sofipin@gmail.com")
    driver.find_element(By.NAME, "contraseniaUsuario").clear()
    driver.find_element(By.NAME, "contraseniaUsuario").send_keys("123")
    driver.find_element(By.XPATH, "//button[contains(text(),'Iniciar Sesión')]").click()
    time.sleep(3)
    cookies = driver.get_cookies()
    session_cookie = None
    for cookie in cookies:
        if cookie['name'] == 'PHPSESSID':
            session_cookie = cookie
            break
    if session_cookie:
        driver.delete_all_cookies()
        driver.add_cookie({
            'name': 'PHPSESSID',
            'value': f"{session_cookie['value']} OR 1=1",
            'domain': 'violet-wolf-820033.hostingersite.com'
        })
        driver.refresh()
        time.sleep(3)
        capturar("04_sql_injection_cookie")
        print("🧨 Prueba SQL Injection simulada realizada.")
    else:
        print("❌ No se encontró cookie de sesión para la prueba SQLi.")

    # 5️⃣ PRUEBA DE CSRF
    print("🔓 Prueba 5: CSRF en cierre de sesión")
    driver.get("https://violet-wolf-820033.hostingersite.com/BackEnd/cerrarsesion.php")
    time.sleep(2)
    capturar("05_csrf")
    print("✅ Prueba CSRF ejecutada.")

except Exception as e:
    print(f"⚠️ Error general: {e}")
    capturar("error_general")

finally:
    time.sleep(2)
    driver.quit()
    print("🚦 Pruebas de seguridad finalizadas.")

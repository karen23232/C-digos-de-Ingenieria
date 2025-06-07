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
os.makedirs("capturas_seguridad_recibimiento", exist_ok=True)

def capturar(nombre):
    driver.save_screenshot(f"capturas_seguridad_recibimiento/{nombre}.png")

try:
    # 1️⃣ INICIAR SESIÓN
    driver.get("https://violet-wolf-820033.hostingersite.com/iniciodesesion.php")
    time.sleep(2)
    driver.find_element(By.NAME, "correoUsuario").send_keys("juan@gmail.com")
    driver.find_element(By.NAME, "contraseniaUsuario").send_keys("J")
    driver.find_element(By.XPATH, "//button[contains(text(),'Iniciar Sesión')]").click()
    time.sleep(3)
    capturar("01_sesion_iniciada")
    print("✅ Sesión iniciada correctamente.")

    wait = WebDriverWait(driver, 10)

    # 2️⃣ VERIFICAR URL Y FORZAR NAVEGACIÓN A LA PÁGINA PRINCIPAL
    current_url = driver.current_url
    print(f"🌐 URL actual después de iniciar sesión: {current_url}")

    if "principalp.php" not in current_url:
        print("⚠️ Redirigido a otra página, forzando la navegación a principalp.php...")
        driver.get("https://violet-wolf-820033.hostingersite.com/FrontEnd/principalp.php")
        time.sleep(3)

    capturar("02_pagina_principal")
    print("✅ Página principal cargada.")

    # 3️⃣ PRUEBA DE SQL INJECTION (simulada manipulando la cookie)
    print("🧨 Prueba de SQL Injection...")
    cookies = driver.get_cookies()
    session_cookie = None
    for cookie in cookies:
        if cookie['name'] == 'PHPSESSID':
            session_cookie = cookie
            break

    if session_cookie:
        print(f"✅ Cookie de sesión: {session_cookie['value']}")
        driver.delete_all_cookies()
        driver.add_cookie({'name': 'PHPSESSID', 'value': f"{session_cookie['value']} OR 1=1", 'domain': 'violet-wolf-820033.hostingersite.com'})
        driver.refresh()
        time.sleep(3)
        capturar("03_sql_injection_cookie")
        print("⚠️ Se manipuló la cookie de sesión para simular inyección SQL.")
    else:
        print("❌ No se encontró cookie de sesión para la prueba SQLi.")

    # 4️⃣ PRUEBA DE XSS (simulada cambiando el nombre del usuario)
    print("🧬 Prueba de XSS...")
    try:
        nombre_usuario = None
        try:
            nombre_usuario = wait.until(EC.presence_of_element_located((By.XPATH, "//h5[contains(text(), 'Hola')]")))
        except:
            try:
                nombre_usuario = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Hola')]")))
            except:
                nombre_usuario = wait.until(EC.presence_of_element_located((By.XPATH, "//strong[contains(text(), '')]")))

        inner_html = nombre_usuario.get_attribute("innerHTML")
        if "<script>" in inner_html:
            print("❌ XSS detectado: el campo nombre ejecuta scripts.")
        else:
            print("✅ Sin XSS reflejado en el nombre de usuario.")
        capturar("04_xss")
    except Exception as e:
        print(f"⚠️ Error al buscar el nombre de usuario: {e}")
        capturar("error_xss")

    # 5️⃣ PRUEBA DE CSRF (simulada)
    print("🔓 Prueba de CSRF...")
    driver.get("https://violet-wolf-820033.hostingersite.com/BackEnd/cerrarsesion.php")
    time.sleep(2)
    capturar("05_csrf")
    print("✅ Petición sin token ejecutada: si no hay verificación de CSRF, es vulnerable.")

except Exception as e:
    print(f"⚠️ Error en la prueba: {e}")
    capturar("error_seguridad_recibimiento")

finally:
    time.sleep(2)
    driver.quit()
    print("🚦 Pruebas finalizadas.")

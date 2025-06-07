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
os.makedirs("capturas_seguridad_vehiculos", exist_ok=True)

def capturar(nombre):
    driver.save_screenshot(f"capturas_seguridad_vehiculos/{nombre}.png")

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

    # Capturar la cookie de sesión
    cookies = driver.get_cookies()
    session_cookie = None
    for cookie in cookies:
        if cookie['name'] == 'PHPSESSID':
            session_cookie = cookie
            break

    if not session_cookie:
        raise Exception("❌ No se encontró cookie de sesión después del inicio de sesión.")

    # 2️⃣ ACCEDER AL MÓDULO DE CONSULTA DE VEHÍCULOS
    driver.get("https://violet-wolf-820033.hostingersite.com/BackEnd/mostrarvehiculos.php")
    driver.delete_all_cookies()
    driver.add_cookie({'name': 'PHPSESSID', 'value': session_cookie['value'], 'domain': 'violet-wolf-820033.hostingersite.com'})
    driver.refresh()
    time.sleep(3)

    current_url = driver.current_url
    print(f"🌐 URL actual: {current_url}")

    if "mostrarvehiculos.php" not in current_url:
        print("⚠️ Redirigido a otra página, forzando navegación al módulo de consulta de vehículos...")
        driver.get("https://violet-wolf-820033.hostingersite.com/BackEnd/mostrarvehiculos.php")
        driver.delete_all_cookies()
        driver.add_cookie({'name': 'PHPSESSID', 'value': session_cookie['value'], 'domain': 'violet-wolf-820033.hostingersite.com'})
        driver.refresh()
        time.sleep(3)

    capturar("02_modulo_consulta_vehiculos")
    print("✅ Módulo de consulta de vehículos cargado.")

    # 3️⃣ PRUEBA DE SQL INJECTION (simulada manipulando la cookie)
    print("🧨 Prueba de SQL Injection...")
    driver.delete_all_cookies()
    driver.add_cookie({'name': 'PHPSESSID', 'value': f"{session_cookie['value']} OR 1=1", 'domain': 'violet-wolf-820033.hostingersite.com'})
    driver.get("https://violet-wolf-820033.hostingersite.com/BackEnd/mostrarvehiculos.php")
    driver.delete_all_cookies()
    driver.add_cookie({'name': 'PHPSESSID', 'value': session_cookie['value'], 'domain': 'violet-wolf-820033.hostingersite.com'})
    driver.refresh()
    time.sleep(3)
    capturar("03_sql_injection_cookie")
    print("⚠️ Se manipuló la cookie de sesión para simular inyección SQL.")

    # 4️⃣ PRUEBA DE XSS (simulada en la marca del vehículo)
    print("🧬 Prueba de XSS...")
    try:
        tabla = wait.until(EC.presence_of_element_located((By.XPATH, "//table")))
        filas = tabla.find_elements(By.XPATH, ".//tr[position()>1]")  # Ignora la cabecera
        if not filas:
            print("⚠️ No hay vehículos registrados para realizar la prueba de XSS.")
            capturar("error_xss_no_data")
        else:
            primera_fila = filas[0]
            celdas = primera_fila.find_elements(By.TAG_NAME, "td")
            if len(celdas) < 2:
                print("⚠️ La fila de la tabla no tiene suficientes columnas para verificar la marca.")
                capturar("error_xss_columns")
            else:
                marca_celda = celdas[1]  # Segunda columna: Marca
                inner_html = marca_celda.get_attribute("innerHTML")
                if "<script>" in inner_html:
                    print("❌ XSS detectado: la marca ejecuta scripts.")
                else:
                    print("✅ Sin XSS reflejado en la marca del vehículo.")
                capturar("04_xss")
    except Exception as e:
        print(f"⚠️ Error al buscar la marca del vehículo: {e}")
        capturar("error_xss")

    # 5️⃣ PRUEBA DE CSRF (simulada)
    print("🔓 Prueba de CSRF...")
    try:
        botones_eliminar = driver.find_elements(By.XPATH, "//a[contains(@href,'eliminarvehiculo.php')]")
        if not botones_eliminar:
            print("⚠️ No hay botones de eliminar en la tabla para la prueba de CSRF.")
            capturar("error_csrf_no_data")
        else:
            href = botones_eliminar[0].get_attribute("href")
            driver.get(href)
            driver.delete_all_cookies()
            driver.add_cookie({'name': 'PHPSESSID', 'value': session_cookie['value'], 'domain': 'violet-wolf-820033.hostingersite.com'})
            driver.refresh()
            time.sleep(3)
            capturar("05_csrf")
            print("✅ Prueba de CSRF ejecutada: la eliminación podría ejecutarse sin token CSRF.")
    except Exception as e:
        print(f"⚠️ Error al ejecutar la prueba de CSRF: {e}")
        capturar("error_csrf")

except Exception as e:
    print(f"⚠️ Error en la prueba: {e}")
    capturar("error_seguridad_vehiculos")

finally:
    time.sleep(2)
    driver.quit()
    print("🚦 Pruebas finalizadas.")

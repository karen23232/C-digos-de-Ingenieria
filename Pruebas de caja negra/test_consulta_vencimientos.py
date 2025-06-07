from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import os

# Ruta al chromedriver (en misma carpeta del script)
RUTA_DRIVER = os.path.join(os.getcwd(), "chromedriver.exe")
service = Service(RUTA_DRIVER)
driver = webdriver.Chrome(service=service)
driver.maximize_window()

try:
    # 1. Ir a la página de inicio de sesión
    driver.get("https://violet-wolf-820033.hostingersite.com/iniciodesesion.php")
    time.sleep(2)

    # 2. Ingresar credenciales con los name correctos
    driver.find_element(By.NAME, "correoUsuario").send_keys("karen@gmail.com")
    driver.find_element(By.NAME, "contraseniaUsuario").send_keys("karen")
    time.sleep(1)

    # 3. Hacer clic en el botón "Iniciar Sesión" por texto del botón
    driver.find_element(By.XPATH, "//button[contains(text(),'Iniciar Sesión')]").click()
    time.sleep(3)

    # 4. Verificar que redirige a la página principal
    assert "paginaprincipal" in driver.current_url
    print("✅ Inicio de sesión exitoso.")

    # 5. Ir al módulo de consulta de vencimientos
    driver.get("https://violet-wolf-820033.hostingersite.com/FrontEnd/consultarvd.php")
    time.sleep(3)

    # 6. Verificar título
    titulo = driver.find_element(By.TAG_NAME, "h1").text
    assert "Consultar Vencimiento de Documentos" in titulo
    print("✅ Página de vencimientos cargada.")

    # 7. Verificar existencia de la tabla
    tabla = driver.find_element(By.TAG_NAME, "table")
    filas = tabla.find_elements(By.TAG_NAME, "tr")
    assert len(filas) > 1
    print(f"✅ Se encontraron {len(filas)-1} filas de documentos.")

    # 8. Detectar alertas si existen
    alertas = driver.find_elements(By.CLASS_NAME, "alerta-item")
    print(f"ℹ️ Se encontraron {len(alertas)} alertas de vencimiento.")

except Exception as e:
    print("❌ Error durante la prueba:", str(e))

finally:
    driver.quit()

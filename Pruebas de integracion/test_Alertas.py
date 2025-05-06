from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import os

# Configurar navegador
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Crear carpeta para capturas
os.makedirs("capturas", exist_ok=True)

def capturar(nombre_archivo):
    ruta = f"capturas/{nombre_archivo}.png"
    driver.save_screenshot(ruta)
    print(f"📸 Captura guardada: {ruta}")

try:
    # 1. Acceder al login
    driver.get("https://violet-wolf-820033.hostingersite.com/iniciodesesion.php")
    time.sleep(2)
    capturar("01_login_cargado")

    # 2. Llenar formulario de login con los datos proporcionados
    driver.find_element(By.ID, "correoUsuario").send_keys("juan@gmail.com")
    driver.find_element(By.ID, "contraseniaUsuario").send_keys("J")
    capturar("02_login_datos_ingresados")

    # 3. Iniciar sesión
    driver.find_element(By.CSS_SELECTOR, "button.btn-custom").click()
    time.sleep(3)
    capturar("03_login_exitoso")

    # 4. Ir a la página de vencimiento de documentos
    driver.get("https://violet-wolf-820033.hostingersite.com/FrontEnd/consultarvd.php")
    time.sleep(4)

    # 5. Scroll hacia la sección de alertas + un poco más para que entren todas
    primer_alerta = driver.find_element(By.CLASS_NAME, "alerta-item")
    driver.execute_script("""
        arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});
        window.scrollBy(0, 100);  // scroll adicional para asegurar que se vean todas
    """, primer_alerta)
    time.sleep(2)
    capturar("04_alertas_completas")

    # 6. Validar cantidad de alertas detectadas
    alertas = driver.find_elements(By.CLASS_NAME, "alerta-item")
    print(f"✅ Se detectaron {len(alertas)} alertas de vencimiento.")

except Exception as e:
    print(f"⚠️ Error durante la ejecución: {e}")
    capturar("error_general")

finally:
    time.sleep(2)
    driver.quit()

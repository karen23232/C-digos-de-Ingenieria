from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import os

# Configuración
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
os.makedirs("capturas", exist_ok=True)

def capturar(nombre):
    path = f"capturas/{nombre}.png"
    driver.save_screenshot(path)
    print(f"📸 Captura: {path}")

def clase_esperada_por_texto(texto):
    texto = texto.lower()
    if "vencido" in texto or "vence hoy" in texto:
        return "table-danger"
    elif "queda 1 día" in texto or "quedan 2 días" in texto or "quedan 3 días" in texto:
        return "table-warning"
    elif "15 días" in texto:
        return "table-info"
    elif "30 días" in texto:
        return "table-success"
    return ""

try:
    # 1. Login
    driver.get("https://violet-wolf-820033.hostingersite.com/iniciodesesion.php")
    time.sleep(2)
    driver.find_element(By.ID, "correoUsuario").send_keys("juan@gmail.com")
    driver.find_element(By.ID, "contraseniaUsuario").send_keys("J")
    driver.find_element(By.CSS_SELECTOR, "button.btn-custom").click()
    time.sleep(3)
    capturar("01_login_exitoso")

    # 2. Ir a alertas
    driver.get("https://violet-wolf-820033.hostingersite.com/FrontEnd/consultarvd.php")
    time.sleep(3)
    capturar("02_alertas_cargadas")

    alertas = driver.find_elements(By.CLASS_NAME, "alerta-item")
    print(f"🔍 {len(alertas)} alertas detectadas.")

    errores = 0
    for alerta in alertas:
        clase = alerta.get_attribute("class")
        texto = alerta.text.lower()
        esperada = clase_esperada_por_texto(texto)

        if esperada and esperada not in clase:
            print(f"❌ ALERTA MAL CLASIFICADA: texto='{texto}' → esperada='{esperada}' pero clase='{clase}'")
            errores += 1
        else:
            print(f"✅ Alerta correcta: '{texto}' → clase: '{clase}'")

    if errores == 0:
        print("✅ TODAS LAS ALERTAS CLASIFICADAS CORRECTAMENTE (según lógica interna)")
    else:
        print(f"⚠️ {errores} alertas tienen clases incorrectas según la lógica PHP")

    capturar("03_alertas_validadas")

except Exception as e:
    print(f"⚠️ ERROR: {e}")
    capturar("error")

finally:
    time.sleep(2)
    driver.quit()

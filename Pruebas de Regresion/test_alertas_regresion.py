from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import re
from collections import Counter

# Configuración del navegador
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
os.makedirs("capturas", exist_ok=True)

def capturar(nombre):
    driver.save_screenshot(f"capturas/{nombre}.png")

try:
    # Iniciar sesión
    driver.get("https://violet-wolf-820033.hostingersite.com/iniciodesesion.php")
    time.sleep(2)
    driver.find_element(By.NAME, "correoUsuario").send_keys("juan@gmail.com")
    driver.find_element(By.NAME, "contraseniaUsuario").send_keys("J")
    driver.find_element(By.XPATH, "//button[contains(text(),'Iniciar Sesión')]").click()
    time.sleep(3)
    capturar("01_sesion_iniciada")

    # Ir a módulo de alertas
    driver.get("https://violet-wolf-820033.hostingersite.com/FrontEnd/consultarvd.php")
    time.sleep(3)
    capturar("02_alertas_cargadas")

    # Verificar panel de alertas
    encabezado = driver.find_element(By.XPATH, "//h5[contains(text(),'Sistema de Alertas de Vencimiento')]")
    assert encabezado.is_displayed(), "❌ No se encontró el encabezado del panel de alertas"
    print("✅ Encabezado del panel de alertas encontrado.")

    # Extraer todas las alertas
    alertas = driver.find_elements(By.CLASS_NAME, "alerta-item")
    total_alertas = len(alertas)
    print(f"📋 Total de alertas encontradas: {total_alertas}")
    capturar("03_alertas_detectadas")

    if total_alertas == 0:
        raise Exception("❌ No hay alertas activas, pero se esperaban algunas.")

    # Analizar contenido de las alertas por tipo
    tipos_detectados = []

    for alerta in alertas:
        texto = alerta.text
        print("🔎 Alerta encontrada:", texto)

        # Buscar palabras clave: SOAT, Tecnomecánica, Licencia
        for tipo in ["SOAT", "Tecnomecánica", "Licencia"]:
            if tipo.lower() in texto.lower():
                tipos_detectados.append(tipo)
                break

    # Contar tipos de alertas
    conteo_tipos = Counter(tipos_detectados)
    print("\n📊 Resumen de alertas por tipo de documento:")
    for tipo, cantidad in conteo_tipos.items():
        print(f" - {tipo}: {cantidad} alerta(s)")

    capturar("04_alertas_por_tipo")

except Exception as e:
    print(f"⚠️ Error en la prueba: {e}")
    capturar("error_alertas")

finally:
    time.sleep(2)
    driver.quit()

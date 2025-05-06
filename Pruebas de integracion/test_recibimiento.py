from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# Ruta local de tu archivo HTML
ruta_local = 'https://violet-wolf-820033.hostingersite.com/'  # <-- cambia esto a tu ruta local

# Configurar el navegador (Chrome)
service = Service('chromedriver.exe')
driver = webdriver.Chrome(service=service)
# Abrir la página de recibimiento
driver.get(ruta_local)
time.sleep(2)

# Verifica que el título de la página sea correcto
assert "Sistema Temprano de Recordatorios y Alertas de tu Vehículo" in driver.title
print("✅ El título se carga correctamente.")

# Verifica que el botón de "Iniciar Sesión" exista
boton_login = driver.find_element(By.LINK_TEXT, "Iniciar Sesión")
assert boton_login is not None
print("✅ Botón 'Iniciar Sesión' encontrado.")

# Verifica que las secciones clave existen
seccion_nosotros = driver.find_element(By.ID, "nosotros")
assert seccion_nosotros is not None
print("✅ Sección '¿Qué es STRAV?' presente.")

# Finaliza la prueba
driver.quit()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import os

# Usar ruta relativa desde el mismo directorio
RUTA_DRIVER = os.path.join(os.getcwd(), "chromedriver.exe")
service = Service(RUTA_DRIVER)
driver = webdriver.Chrome(service=service)

# Acceder a la página
driver.get("https://violet-wolf-820033.hostingersite.com/")
driver.maximize_window()
time.sleep(2)

# Prueba: Verifica el título de la página
assert "Sistema Temprano de Recordatorios y Alertas" in driver.title
print("✅ Título verificado")

# Prueba: Botón de 'Iniciar Sesión'
boton_login = driver.find_element(By.LINK_TEXT, "Iniciar Sesión")
assert boton_login is not None
print("✅ Botón de Iniciar Sesión encontrado")

# Prueba: Redirección al registro
boton_registro = driver.find_element(By.LINK_TEXT, "Registrarse")
boton_registro.click()
time.sleep(2)
print("✅ Redirección a página de registro")

# Cerrar
driver.quit()

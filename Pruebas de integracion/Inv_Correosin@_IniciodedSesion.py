
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

# Configurar WebDriver
service = Service()
driver = webdriver.Chrome(service=service)
driver.get("https://violet-wolf-820033.hostingersite.com/iniciodesesion.php")
time.sleep(1)

# Localizar campos
correo_input = driver.find_element(By.NAME, "correoUsuario")
contrasena_input = driver.find_element(By.NAME, "contraseniaUsuario")
submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")

# Ingresar correo inválido (sin @) y contraseña válida
correo_input.send_keys("jackgmail.com")
contrasena_input.send_keys("123")

# Intentar hacer submit con JavaScript para evitar que Selenium lo bloquee
driver.execute_script("arguments[0].click();", submit_button)

# Verificar si el input es inválido
es_invalido = driver.execute_script("return arguments[0].validity.valid;", correo_input)

if not es_invalido:
    print("✅ Validación del '@' en correo detectada correctamente.")
else:
    print("❌ El navegador no bloqueó el correo inválido como se esperaba.")

# Esperar para visualización humana (opcional)
time.sleep(2)

driver.quit()

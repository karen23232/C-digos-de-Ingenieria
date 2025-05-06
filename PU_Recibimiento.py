
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# URLs correctas
URL_BASE = "https://violet-wolf-820033.hostingersite.com/"
URL_REGISTRO_ESPERADA = URL_BASE + "registro.html"
URL_LOGIN_ESPERADA = URL_BASE + "iniciodesesion.php"

# Iniciar el navegador
driver = webdriver.Chrome()

try:
    driver.get(URL_BASE)
    time.sleep(2)  # Esperar que cargue

    exito_registro = False
    exito_login = False

    # --- Probar botón "Registrarse" ---
    try:
        boton_registro = driver.find_element(By.LINK_TEXT, "Registrarse")
        boton_registro.click()
        time.sleep(2)
        if driver.current_url == URL_REGISTRO_ESPERADA:
            print("✅ Redirección a 'Registrarse' exitosa.")
            exito_registro = True
        else:
            print(f"❌ Redirección a 'Registrarse' fallida. URL actual: {driver.current_url}")
    except Exception as e:
        print("❌ Error al hacer clic en 'Registrarse':", e)

    # Volver a la página principal
    driver.get(URL_BASE)
    time.sleep(2)

    # --- Probar botón "Iniciar Sesión" ---
    try:
        boton_login = driver.find_element(By.LINK_TEXT, "Iniciar Sesión")
        boton_login.click()
        time.sleep(2)
        if driver.current_url == URL_LOGIN_ESPERADA:
            print("✅ Redirección a 'Iniciar Sesión' exitosa.")
            exito_login = True
        else:
            print(f"❌ Redirección a 'Iniciar Sesión' fallida. URL actual: {driver.current_url}")
    except Exception as e:
        print("❌ Error al hacer clic en 'Iniciar Sesión':", e)

    # Resultado final
    if exito_registro and exito_login:
        print("🎉 Prueba pasada: ambas redirecciones funcionan correctamente.")
    else:
        print("⚠️ Prueba incompleta: al menos una redirección falló.")

finally:
    driver.quit()

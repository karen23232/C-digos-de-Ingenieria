from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configurar el navegador (usamos Chrome)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

try:
    # Abrir la página inicial
    driver.get("https://violet-wolf-820033.hostingersite.com/iniciodesesion.php")

    # Esperar a que aparezca el campo de correo
    correo_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "correoUsuario"))
    )
    correo_input.send_keys("sofipin@gmail.com")

    # Llenar el campo de contraseña
    contrasenia_input = driver.find_element(By.ID, "contraseniaUsuario")
    contrasenia_input.send_keys("123")

    # Esperar a que el botón de submit esté disponible y hacer scroll
    btn_submit = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "btnSubmit"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", btn_submit)
    btn_submit.click()

    # Esperar a que cambie la URL después del login (puedes ajustar la URL esperada)
    WebDriverWait(driver, 10).until(EC.url_contains("paginaprincipal"))

    # Esperar por el botón Consultar Vencimientos
    btn_consultar_venc = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "btnConsultarVenc"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_consultar_venc)
    WebDriverWait(driver, 2).until(EC.visibility_of(btn_consultar_venc))  # por si tarda en mostrarse del todo
    driver.execute_script("arguments[0].click();", btn_consultar_venc)

    # Esperar a que cargue la página de consulta
    WebDriverWait(driver, 10).until(EC.url_contains("consultarvd.php"))

    # Esperar a que se cargue la tabla
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//table[@class='table table-hover table-striped']"))
    )

    # Obtener todas las fechas de vencimiento antes de la modificación
    fechas_vencimiento = driver.find_elements(By.XPATH, "//td[normalize-space()]")  # Todas las celdas en la columna de fechas
    fechas_originales = [fecha.text for fecha in fechas_vencimiento]
    print("\n// Fechas de vencimiento iniciales:", fechas_originales)

    # Esperar un tiempo para que puedas modificar manualmente la fecha
    print("\n// Esperando 30 segundos para que puedas modificar manualmente el campo de fecha...\n")
    time.sleep(30)  # Espera 30 segundos para la interacción manual

    # Obtener las fechas de vencimiento después de la modificación
    fechas_vencimiento_actualizadas = driver.find_elements(By.XPATH, "//td[normalize-space()]")
    fechas_actualizadas = [fecha.text for fecha in fechas_vencimiento_actualizadas]
    print("\n// Fechas de vencimiento después de la modificación:", fechas_actualizadas)

    # Verificar si alguna fecha cambió
    cambios_detectados = False
    for i in range(len(fechas_originales)):
        if fechas_originales[i] != fechas_actualizadas[i]:
            print("")
            print(f"// Fecha cambiada de {fechas_originales[i]} a {fechas_actualizadas[i]}")
            cambios_detectados = True

    if not cambios_detectados:
        print("// No se detectaron cambios en las fechas de vencimiento.")

    if cambios_detectados:
        print("// ✅ Prueba exitosa.")

finally:
    driver.quit()

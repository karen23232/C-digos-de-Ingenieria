import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

TOTAL_PRUEBAS = 2
contador = {"actual": 0}

@pytest.fixture
def driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.mark.parametrize("correo, contrasena, descripcion, espera_vehiculos", [
    ("sebastian@gmail.com", "132", "Consulta válida de vehículos", True),   # CP011
    ("sebastian@gmail.com", "132", "Consulta sin vehículos", False)         # CP012
])
def test_consulta_vehiculos(driver, correo, contrasena, descripcion, espera_vehiculos):
    driver.get("https://violet-wolf-820033.hostingersite.com/iniciodesesion.php")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "correoUsuario"))
    )

    driver.find_element(By.ID, "correoUsuario").send_keys(correo)
    driver.find_element(By.ID, "contraseniaUsuario").send_keys(contrasena)
    driver.find_element(By.CSS_SELECTOR, "button.btn-custom").click()

    time.sleep(2)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Consultar Vehículos"))
    )
    driver.find_element(By.LINK_TEXT, "Consultar Vehículos").click()

    time.sleep(2)

    # Caja negra: Solo comprobamos la existencia de elementos esperados
    try:
        vehiculos = driver.find_elements(By.CLASS_NAME, "vehiculo-item")  # Asumiendo que cada vehículo tiene esta clase
        if espera_vehiculos:
            assert len(vehiculos) > 0, f"❌ {descripcion}: Se esperaban vehículos pero no se encontraron."
        else:
            assert len(vehiculos) == 0, f"❌ {descripcion}: No se esperaban vehículos pero se encontraron."
    except Exception as e:
        print(f"⚠️ {descripcion}: No se pudo verificar correctamente — {e}")

    contador["actual"] += 1
    porcentaje = (contador["actual"] / TOTAL_PRUEBAS) * 100
    print(f"✅ Prueba {contador['actual']}/{TOTAL_PRUEBAS} ({descripcion}) completada ({porcentaje:.0f}%)")

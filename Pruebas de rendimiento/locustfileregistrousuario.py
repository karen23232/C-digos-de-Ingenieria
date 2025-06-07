import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

TOTAL_PRUEBAS = 7
contador = {"actual": 0}

@pytest.fixture
def driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.mark.parametrize("nombre, correo, contrasena, descripcion", [
    ("sebastian", "sebastian@gmail.com", "1234", "CP018: Registro válido"),
    ("sebastian", "lorem@gmail.com", "1234", "CP019: Usuario repetido"),
    ("laurencia", "sebastian@gmail.com", "1234", "CP020: Correo repetido"),
    ("kevin", "kevin@gmail.com", "1234", "CP021: Usuario y correo repetidos"),
    ("rene", "", "Ka._n18!", "CP022: Correo vacío"),
    ("lorena", "lorena@gmail.com", "", "CP023: Contraseña vacía"),
    ("", "sofuedapin@gmail.com", "Ka._n18!", "CP024: Nombre vacío")
])
def test_registro_parametrizado(driver, nombre, correo, contrasena, descripcion):
    inicio_total = time.time()

    driver.get("https://violet-wolf-820033.hostingersite.com/registro.html")
    inicio_carga = time.time()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "nombreUsuario"))
    )
    fin_carga = time.time()
    tiempo_carga = fin_carga - inicio_carga

    if nombre:
        driver.find_element(By.ID, "nombreUsuario").send_keys(nombre)
    if correo:
        driver.find_element(By.ID, "correoUsuario").send_keys(correo)
    if contrasena:
        driver.find_element(By.ID, "contraseniaUsuario").send_keys(contrasena)

    inicio_envio = time.time()
    driver.find_element(By.CSS_SELECTOR, "button.btn-custom").click()
    time.sleep(1)
    fin_envio = time.time()
    tiempo_envio = fin_envio - inicio_envio

    fin_total = time.time()
    tiempo_total = fin_total - inicio_total

    contador["actual"] += 1
    porcentaje = (contador["actual"] / TOTAL_PRUEBAS) * 100

    print(f"\n✅ Prueba {contador['actual']}/{TOTAL_PRUEBAS} ({descripcion}) completada ({porcentaje:.0f}%)")
    print(f"📊 Tiempo de carga: {tiempo_carga:.2f}s | Tiempo de envío: {tiempo_envio:.2f}s | Tiempo total: {tiempo_total:.2f}s\n")

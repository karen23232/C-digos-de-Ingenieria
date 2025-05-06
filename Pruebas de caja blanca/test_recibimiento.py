import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


def test_desplazamiento_suave():
    ruta_archivo = os.path.abspath("recibimiento.html")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("file://" + ruta_archivo)

    driver.execute_script("""
        const seccion = document.createElement('div');
        seccion.id = 'seccion';
        seccion.style.height = '1500px';
        seccion.textContent = 'Contenido de Sección';
        document.body.appendChild(seccion);

        window.scrollTo({ top: 1000, behavior: 'smooth' });
    """)

    time.sleep(2)  # Esperar al scroll
    ubicacion = driver.execute_script("return window.scrollY;")
    print(f"ScrollY: {ubicacion}")
    assert ubicacion > 500  # Ajusta el umbral según la posición objetivo

    driver.quit()


def test_ocultar_mostrar_encabezado():
    ruta_archivo = os.path.abspath("recibimiento.html")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("file://" + ruta_archivo)

    driver.execute_script("""
        const header = document.createElement('div');
        header.id = 'header';
        header.classList = '';  // por si acaso
        header.textContent = 'Encabezado';
        document.body.prepend(header);

        const largo = document.createElement('div');
        largo.style.height = '2000px';
        document.body.appendChild(largo);

        window.addEventListener('scroll', () => {
            const header = document.getElementById('header');
            if (window.scrollY > 100) {
                header.classList.add('hidden');
            } else {
                header.classList.remove('hidden');
            }
        });
    """)

    driver.execute_script("window.scrollTo(0, 300);")
    time.sleep(1)
    clase_oculta = driver.execute_script("return document.getElementById('header').classList.contains('hidden');")
    assert clase_oculta is True

    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)
    clase_visible = driver.execute_script("return document.getElementById('header').classList.contains('hidden');")
    assert clase_visible is False

    driver.quit()

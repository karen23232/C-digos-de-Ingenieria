import pytest
from app import app
import sys

# Colores para la consola
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_test_result(test_name, expected, actual, passed):
    bg_color = Colors.GREEN if passed else Colors.RED
    result_text = "CORRECTO" if passed else "INCORRECTO"
    print(f"\n{Colors.BOLD}▶ {test_name}{Colors.ENDC}")
    print(f"{bg_color}▶ Resultado esperado: {expected} | Resultado obtenido: {actual} | {result_text}{Colors.ENDC}")

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_validar_pico_y_placa_restriccion(client):
    response = client.post('/validar_pico_y_placa', json={
        "placa": "XYZ456",
        "fecha": "2025-04-23"
    })
    expected_pico_placa = True
    actual_pico_placa = response.json['pico_placa']
    passed = expected_pico_placa == actual_pico_placa
    print_test_result("Probando restricción de Pico y Placa",
                     f"pico_placa: {expected_pico_placa}",
                     f"pico_placa: {actual_pico_placa}",
                     passed)
    assert response.status_code == 200, "La respuesta debería ser 200 OK"
    assert actual_pico_placa == expected_pico_placa, "Debe tener restricción de Pico y Placa"
    expected_mensaje = "No puedes circular el 2025-04-23."
    actual_mensaje = response.json['mensaje']
    passed_mensaje = expected_mensaje == actual_mensaje
    print_test_result("Probando mensaje de restricción",
                     expected_mensaje,
                     actual_mensaje,
                     passed_mensaje)
    assert actual_mensaje == expected_mensaje, "El mensaje de Pico y Placa es incorrecto"
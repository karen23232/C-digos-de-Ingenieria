import pytest
from app import app
import sys

# Colores para consola
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

def print_test_result(test_name, expected, actual, passed):
    color = Colors.GREEN if passed else Colors.RED
    result_text = "CORRECTO" if passed else "INCORRECTO"
    print(f"\n{Colors.BOLD}▶ {test_name}{Colors.ENDC}")
    print(f"{color}▶ Esperado: {expected} | Obtenido: {actual} | {result_text}{Colors.ENDC}")

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_regresion_pico_y_placa(client):
    """Prueba de regresión para validar que las respuestas conocidas no cambien."""
    casos_historicos = [
        {
            "input": {"placa": "XYZ456", "fecha": "2025-04-23"},
            "expected": {
                "status_code": 200,
                "pico_placa": True,
                "mensaje": "No puedes circular el 2025-04-23."
            }
        },
        {
            "input": {"placa": "XYZ456", "fecha": "2025-04-24"},
            "expected": {
                "status_code": 200,
                "pico_placa": False,
                "mensaje": "Puedes circular el 2025-04-24."
            }
        },
        {
            "input": {"placa": "XYZ456", "fecha": "2025-04-26"},
            "expected": {
                "status_code": 200,
                "pico_placa": False,
                "mensaje": "Puedes circular el 2025-04-26. Es fin de semana."
            }
        }
    ]

    for caso in casos_historicos:
        response = client.post('/validar_pico_y_placa', json=caso["input"])
        expected = caso["expected"]

        # Validar status code
        passed_status = response.status_code == expected["status_code"]
        print_test_result("Status Code", expected["status_code"], response.status_code, passed_status)
        assert passed_status, f"Status Code incorrecto para {caso['input']}"

        # Validar pico_placa
        actual_pico_placa = response.json["pico_placa"]
        passed_pico_placa = actual_pico_placa == expected["pico_placa"]
        print_test_result("Resultado Pico y Placa", expected["pico_placa"], actual_pico_placa, passed_pico_placa)
        assert passed_pico_placa, f"Resultado Pico y Placa incorrecto para {caso['input']}"

        # Validar mensaje
        actual_mensaje = response.json["mensaje"]
        passed_mensaje = actual_mensaje == expected["mensaje"]
        print_test_result("Mensaje Pico y Placa", expected["mensaje"], actual_mensaje, passed_mensaje)
        assert passed_mensaje, f"Mensaje incorrecto para {caso['input']}"

if __name__ == "__main__":
    client = app.test_client()
    test_regresion_pico_y_placa(client)

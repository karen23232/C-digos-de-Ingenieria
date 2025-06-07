import pytest
import time
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_registrar_vehiculo(client):
    """Prueba que un vehículo se registre correctamente y mida el tiempo de respuesta."""
    inicio = time.time()
    response = client.post('/registrar_vehiculo', json={
        "marcaVeh": "Mazda",
        "placaVeh": "JKL789",
        "imagen": "mazda.jpg"
    })
    fin = time.time()
    tiempo = fin - inicio

    assert response.status_code == 201, "Debe retornar 201 Created"
    data = response.get_json()
    assert data["mensaje"] == "Vehículo registrado exitosamente.", "Mensaje de registro incorrecto"
    assert data["vehiculo"]["marcaVeh"] == "Mazda", "Marca incorrecta en el registro"
    assert data["vehiculo"]["placaVeh"] == "JKL789", "Placa incorrecta en el registro"
    assert data["vehiculo"]["imagen"] == "mazda.jpg", "Imagen incorrecta en el registro"

    print(f"✅ test_registrar_vehiculo completado en {tiempo:.4f} segundos.")

def test_consultar_vehiculos(client):
    """Prueba que la consulta de vehículos retorne una lista no vacía y mida el tiempo."""
    inicio = time.time()
    response = client.get('/vehiculos')
    fin = time.time()
    tiempo = fin - inicio

    assert response.status_code == 200, "Debe retornar 200 OK"
    data = response.get_json()
    assert isinstance(data, list), "Debe retornar una lista"
    assert len(data) >= 2, "Debe haber al menos dos vehículos inicialmente"

    print(f"✅ test_consultar_vehiculos completado en {tiempo:.4f} segundos.")

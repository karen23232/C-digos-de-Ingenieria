import pytest
from datetime import datetime, timedelta
from documentos import dias_restantes, get_alerta_clase, get_alerta_mensaje

def test_dias_restantes():
    hoy = datetime.now().strftime("%Y-%m-%d")
    mañana = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    ayer = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    assert dias_restantes(hoy) == 0
    assert dias_restantes(mañana) == 1
    assert dias_restantes(ayer) == -1
    assert dias_restantes(None) is None

def test_get_alerta_clase():
    assert get_alerta_clase(-5) == "table-danger"
    assert get_alerta_clase(0) == "table-warning"
    assert get_alerta_clase(3) == "table-warning"
    assert get_alerta_clase(10) == "table-info"
    assert get_alerta_clase(20) == "table-success"
    assert get_alerta_clase(31) == ""
    assert get_alerta_clase(None) == ""

def test_get_alerta_mensaje():
    tipo_doc = "SOAT"

    assert get_alerta_mensaje(-5, tipo_doc) == "¡SOAT VENCIDO! Han pasado 5 días."
    assert get_alerta_mensaje(0, tipo_doc) == "¡ATENCIÓN! SOAT vence HOY."
    assert get_alerta_mensaje(1, tipo_doc) == "¡ATENCIÓN! Solo queda 1 día para el vencimiento del SOAT."
    assert get_alerta_mensaje(3, tipo_doc) == "¡ATENCIÓN! Quedan 3 días para el vencimiento del SOAT."
    assert get_alerta_mensaje(10, tipo_doc) == "Atención: Quedan 10 días para el vencimiento del SOAT."
    assert get_alerta_mensaje(20, tipo_doc) == "Atención: Quedan 20 días para el vencimiento del SOAT."
    assert get_alerta_mensaje(40, tipo_doc) == ""
    assert get_alerta_mensaje(None, tipo_doc) == ""

# test_logica_documentos_pytest.py
from datetime import datetime, timedelta

# Mismas funciones del código original
def dias_restantes(fecha_str):
    if not fecha_str:
        return None
    hoy = datetime.today().date()
    fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
    return (fecha - hoy).days

def alerta_clase(dias):
    if dias is None:
        return ""
    if dias < 0:
        return "table-danger"
    elif dias <= 5:
        return "table-warning"
    elif dias <= 15:
        return "table-info"
    elif dias <= 30:
        return "table-success"
    return ""

def alerta_mensaje(dias, tipo_doc):
    if dias is None:
        return ""
    if dias < 0:
        return f"¡{tipo_doc} VENCIDO! Han pasado {abs(dias)} días."
    elif dias == 0:
        return f"¡ATENCIÓN! {tipo_doc} vence HOY."
    elif dias == 1:
        return f"¡ATENCIÓN! Solo queda 1 día para el vencimiento del {tipo_doc}."
    elif dias <= 5:
        return f"¡ATENCIÓN! Quedan {dias} días para el vencimiento del {tipo_doc}."
    elif dias <= 15 or dias <= 30:
        return f"Atención: Quedan {dias} días para el vencimiento del {tipo_doc}."
    return ""

# ---- Pruebas con pytest ----

def test_dias_restantes():
    hoy = datetime.today().date()
    assert dias_restantes(hoy.strftime("%Y-%m-%d")) == 0
    assert dias_restantes((hoy + timedelta(days=3)).strftime("%Y-%m-%d")) == 3
    assert dias_restantes((hoy - timedelta(days=5)).strftime("%Y-%m-%d")) == -5

def test_alerta_clase():
    assert alerta_clase(-3) == "table-danger"
    assert alerta_clase(4) == "table-warning"
    assert alerta_clase(10) == "table-info"
    assert alerta_clase(20) == "table-success"
    assert alerta_clase(40) == ""
    assert alerta_clase(None) == ""

def test_alerta_mensaje():
    assert alerta_mensaje(-2, "SOAT") == "¡SOAT VENCIDO! Han pasado 2 días."
    assert alerta_mensaje(0, "Tecnomecánica") == "¡ATENCIÓN! Tecnomecánica vence HOY."
    assert alerta_mensaje(1, "Licencia") == "¡ATENCIÓN! Solo queda 1 día para el vencimiento del Licencia."
    assert alerta_mensaje(5, "SOAT") == "¡ATENCIÓN! Quedan 5 días para el vencimiento del SOAT."
    assert alerta_mensaje(13, "SOAT") == "Atención: Quedan 13 días para el vencimiento del SOAT."
    assert alerta_mensaje(None, "Licencia") == ""

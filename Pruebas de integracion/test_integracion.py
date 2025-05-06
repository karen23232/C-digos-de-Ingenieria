from datetime import datetime, timedelta
from vencimiento import DocumentoVehiculo, Vehiculo

def test_documento_vigente():
    print("▶ Ejecutando prueba: Documento vigente...")
    vehiculo = Vehiculo("ABC123")
    futuro = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    doc = DocumentoVehiculo("SOAT", futuro)
    vehiculo.agregar_documento(doc)

    assert len(vehiculo.documentos_vencidos()) == 0, "❌ El documento no debería estar vencido"
    assert len(vehiculo.documentos_vigentes()) == 1, "❌ Debería haber un documento vigente"
    print("✅ Prueba 'documento vigente' pasada.\n")


def test_documento_vencido():
    print("▶ Ejecutando prueba: Documento vencido...")
    vehiculo = Vehiculo("XYZ789")
    pasado = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")
    doc = DocumentoVehiculo("Revisión Técnico Mecánica", pasado)
    vehiculo.agregar_documento(doc)

    assert len(vehiculo.documentos_vencidos()) == 1, "❌ Debería haber un documento vencido"
    assert len(vehiculo.documentos_vigentes()) == 0, "❌ No debería haber documentos vigentes"
    print("✅ Prueba 'documento vencido' pasada.\n")


def test_actualizacion_documento():
    print("▶ Ejecutando prueba: Actualización de documento vencido...")
    vehiculo = Vehiculo("LMN456")
    pasado = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
    doc = DocumentoVehiculo("Licencia", pasado)
    vehiculo.agregar_documento(doc)

    assert doc.esta_vencido(), "❌ El documento debería estar vencido inicialmente"

    # Simulamos actualización
    doc.fecha_vencimiento = datetime.now() + timedelta(days=10)

    assert not doc.esta_vencido(), "❌ El documento ya no debería estar vencido"
    print("✅ Prueba 'actualización de documento' pasada.\n")


# Ejecución manual de las pruebas
if __name__ == "__main__":
    try:
        test_documento_vigente()
        test_documento_vencido()
        test_actualizacion_documento()
        print("🎉 TODAS LAS PRUEBAS DE INTEGRACIÓN PASARON CORRECTAMENTE ✅")
    except AssertionError as error:
        print(str(error))
        print("❌ Alguna prueba falló.")

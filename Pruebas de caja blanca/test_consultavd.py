import mysql.connector
from datetime import datetime, timedelta

# Conexión a la base de datos MySQL
def conectar_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="u598872392_stravhostiger1"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error de conexión: {err}")
        return None

# Funciones para calcular días restantes y generar alerta
# Estas funciones reflejan las funciones presentes en consultarvd.php
def obtener_dias_restantes(fecha_vencimiento):
    hoy = datetime.today().date()
    return (fecha_vencimiento - hoy).days

def generar_mensaje_alerta(dias_restantes):
    if dias_restantes > 30:
        return "El documento está vigente"
    elif dias_restantes >= 15:
        return f"Faltan {dias_restantes} días para vencer"
    elif dias_restantes >= 0:
        return f"¡Atención! El documento vence en {dias_restantes} días"
    else:
        return "¡El documento ha vencido!"

def obtener_clase_alerta(dias_restantes):
    if dias_restantes > 30:
        return "table-success"
    elif dias_restantes >= 15:
        return "table-warning"
    elif dias_restantes >= 0:
        return "table-danger"
    else:
        return "table-danger"

# Función principal de ejecución
def main():
    db_connection = conectar_db()
    if db_connection:
        cursor = db_connection.cursor()

        cursor.execute("""
            SELECT D.fechaVencimiento, D.tipoDoc
            FROM DocumentoVehiculo D
            LEFT JOIN Vehiculo V ON D.idVeh = V.idVeh
            WHERE V.idUsuario = %s AND D.tipoDoc IN ('SOAT', 'Tecnomecánica', 'Licencia')
        """, (1,))

        documentos = cursor.fetchall()

        if documentos:
            for doc in documentos:
                fecha_vencimiento = doc[0]
                tipo_doc = doc[1]
                dias_restantes = obtener_dias_restantes(fecha_vencimiento)

                mensaje = generar_mensaje_alerta(dias_restantes)
                clase_alerta = obtener_clase_alerta(dias_restantes)

                print(f"Documento: {tipo_doc}")
                print(f"Fecha de vencimiento: {fecha_vencimiento}")
                print(f"Días restantes: {dias_restantes}")
                print(f"Mensaje: {mensaje}")
                print(f"Clase de alerta: {clase_alerta}")
                print("-" * 30)
            
            print("✅ Prueba exitosa: los documentos se analizaron correctamente.")
        else:
            print("⚠️ No se encontraron documentos para el usuario.")

        cursor.close()
        db_connection.close()
    else:
        print("❌ No se pudo establecer conexión con la base de datos.")

if __name__ == "__main__":
    main()

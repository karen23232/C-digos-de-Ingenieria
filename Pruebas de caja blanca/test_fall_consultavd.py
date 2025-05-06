import requests

# URL del archivo PHP
url = "http://localhost/strav/consultarvd.php"

# Simulación de sesión para un usuario con idUsuario = 129
session = requests.Session()

# Simulamos que el usuario ha iniciado sesión y tiene idUsuario = 129
# Para pruebas locales, podrías establecer la sesión con un cookie, pero para simplificar, se asume que la sesión ya está activa.

# Simulamos una respuesta con un usuario autenticado
session.cookies.set('idUsuario', '129')

# Realizamos la solicitud GET al script PHP
response = session.get(url)

# Verificamos el código de estado de la respuesta
if response.status_code == 200:
    print("✅ La solicitud fue exitosa.")
else:
    print(f"Error al realizar la solicitud: {response.status_code}")

# Analizar la respuesta HTML (si es necesario para verificar contenido específico)
from bs4 import BeautifulSoup

soup = BeautifulSoup(response.text, 'html.parser')

# Verificamos si la página contiene una tabla con los documentos del vehículo
table = soup.find('table')
if table:
    print("Tabla de vehículos encontrada.")
else:
    print("No se encontró la tabla de vehículos para el usuario.")

# Buscamos mensajes de alerta, que es un indicador de que el sistema está evaluando los vencimientos
alert_messages = soup.find_all('div', class_='mensaje')
for msg in alert_messages:
    print("Mensaje de alerta:", msg.text)

# En este punto podrías añadir más verificaciones dependiendo de la lógica de tu aplicación.

from locust import HttpUser, task, between
from bs4 import BeautifulSoup

class ConsultaDocumentosUser(HttpUser):
    wait_time = between(1, 3)  # Simula el tiempo entre las peticiones

    def on_start(self):
        """Se ejecuta al iniciar la prueba, sirve para hacer login."""
        login_url = "/BackEnd/iniciarsesion.php"  # Ajusta si es necesario
        credentials = {
            "correoUsuario": "karen@gmail.com",
            "contraseniaUsuario": "karen"
        }
        with self.client.post(login_url, data=credentials, catch_response=True) as response:
            if "incorrecta" in response.text or "incorrecto" in response.text:
                response.failure("❌ Error de login.")
            else:
                response.success()

    @task
    def consultar_documentos(self):
        """Simula la consulta de vencimientos de documentos"""
        with self.client.get("/FrontEnd/consultarvd.php", catch_response=True) as response:
            if response.status_code != 200 or "Documentos de Vehículos Registrados" not in response.text:
                response.failure("❌ No se pudo consultar documentos.")
            else:
                response.success()

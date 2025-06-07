from locust import HttpUser, task, between

class ConsultarVehiculosUser(HttpUser):
    wait_time = between(1, 3)  # Simula un usuario que espera entre 1 y 3 segundos

    def on_start(self):
        """Se ejecuta al iniciar la prueba para loguearse."""
        login_url = "/BackEnd/iniciarsesion.php"  # Ajusta según la estructura de tu app
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
    def consultar_vehiculos(self):
        """Simula la consulta de vehículos tras iniciar sesión."""
        with self.client.get("/BackEnd/mostrarvehiculos.php", catch_response=True) as response:
            if response.status_code != 200 or "Mis Vehículos" not in response.text:
                response.failure("❌ No se pudo consultar vehículos.")
            else:
                response.success()

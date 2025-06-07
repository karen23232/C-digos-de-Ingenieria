from locust import HttpUser, task, between

class PruebaAlertas(HttpUser):
    wait_time = between(1, 3)  # tiempo de espera entre cada tarea

    def on_start(self):
        """Inicia sesión y guarda la cookie."""
        response = self.client.post("/iniciodesesion.php", {
            "correoUsuario": "juan@gmail.com",
            "contraseniaUsuario": "J"
        }, allow_redirects=True)
        if response.status_code == 200:
            print("✅ Inicio de sesión exitoso.")
        else:
            print(f"❌ Error al iniciar sesión. Código: {response.status_code}")

    @task
    def consultar_alertas(self):
        """Prueba de rendimiento del módulo de alertas."""
        with self.client.get("/BackEnd/consultarvd.php", catch_response=True) as response:
            if response.status_code == 200 and "Sistema de Alertas de Vencimiento" in response.text:
                response.success()
            else:
                response.failure(f"⚠️ Error al cargar las alertas. Código: {response.status_code}")

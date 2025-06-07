from locust import HttpUser, task, between

class LoginUser(HttpUser):
    wait_time = between(1, 3)  # Simula el tiempo de espera entre las solicitudes

    @task
    def login(self):
        # Ajusta estos datos al formulario real
        payload = {
            "correoUsuario": "karen@gmail.com",
            "contraseniaUsuario": "karen"
        }

        with self.client.post(
            "/BackEnd/iniciarsesion.php",
            data=payload,
            catch_response=True
        ) as response:
            if "Contraseña incorrecta" in response.text or "Usuario incorrecto" in response.text:
                response.failure("Inicio de sesión fallido")
            else:
                response.success()

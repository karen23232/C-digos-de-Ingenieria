import requests
from bs4 import BeautifulSoup

# URLs base y rutas específicas según tu petición
BASE_URL = "https://violet-wolf-820033.hostingersite.com"
LOGIN_PAGE_URL = f"https://violet-wolf-820033.hostingersite.com/iniciodesesion.php"
LOGIN_POST_URL = f"https://violet-wolf-820033.hostingersite.com/BackEnd/iniciarsesion.php"
PRINCIPAL_URL = f"https://violet-wolf-820033.hostingersite.com/FrontEnd/paginaprincipal.php"
CONSULTA_URL = f"https://violet-wolf-820033.hostingersite.com/FrontEnd/consultarvd.php"

# Credenciales válidas
usuario = "karen@gmail.com"
contrasena = "karen"

def login(session):
    # 1. Obtener la página de login para iniciar sesión y cookies
    resp_login_page = session.get(LOGIN_PAGE_URL)
    resp_login_page.raise_for_status()

    # 2. Enviar POST con credenciales a la URL que procesa el login
    payload = {
        "correoUsuario": usuario,
        "contraseniaUsuario": contrasena
    }

    resp_login_post = session.post(LOGIN_POST_URL, data=payload)
    resp_login_post.raise_for_status()

    print("URL después POST login:", resp_login_post.url)
    print("Primeros 500 caracteres de la respuesta login:")
    print(resp_login_post.text[:500])

    # Validar si el login falló
    if "incorrecta" in resp_login_post.text.lower() or "error" in resp_login_post.text.lower():
        print("❌ Login fallido: usuario o contraseña incorrectos")
        return False

    print("✅ Login exitoso y sesión iniciada")
    return True

def acceder_principal(session):
    # Acceder a la página principal después del login
    resp = session.get(PRINCIPAL_URL)
    resp.raise_for_status()
    print("Accedió a la página principal con código:", resp.status_code)
    return True

def acceder_modulo_consulta(session):
    # Acceder al módulo consulta de vencimiento de documentos
    resp = session.get(CONSULTA_URL)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    titulo = soup.find('h1')
    if titulo and "Consultar Vencimiento" in titulo.text:
        print("✅ Acceso a módulo consultarvd.php exitoso")
        return True
    else:
        print("❌ No se pudo acceder correctamente al módulo de consulta")
        return False

def main():
    with requests.Session() as session:
        if login(session):
            acceder_principal(session)
            acceder_modulo_consulta(session)

if __name__ == "__main__":
    main()

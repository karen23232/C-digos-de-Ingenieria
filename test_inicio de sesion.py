# test_auth.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import unittest
from auth import validar_credenciales

class TestAuth(unittest.TestCase):

    def test_usuario_no_existe(self):
        resultado = validar_credenciales("inexistente@gmail.com", "1234")
        print("\n🔎 Probando con usuario NO registrado...")
        print(f"   ➤ Resultado esperado: user_not_found | Resultado obtenido: {resultado}")
        self.assertEqual(resultado, "user_not_found")

    def test_contrasena_incorrecta(self):
        resultado = validar_credenciales("karen@gmail.com", "incorrecta")
        print("\n🔐 Probando con contraseña INCORRECTA...")
        print(f"   ➤ Resultado esperado: incorrect_password | Resultado obtenido: {resultado}")
        self.assertEqual(resultado, "incorrect_password")

    def test_inicio_sesion_exitoso(self):
        resultado = validar_credenciales("juan@gmail.com", "juan")
        print("\n✅ Probando inicio de sesión con datos CORRECTOS...")
        print(f"   ➤ Resultado esperado: login_success | Resultado obtenido: {resultado}")
        self.assertEqual(resultado, "login_success")

# Mensaje final si todos los tests pasan
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestAuth))
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    result = runner.run(suite())
    if result.wasSuccessful():
        print("\n🎉 TODOS LOS TESTS PASARON CORRECTAMENTE 🎉")
    else:
        print("\n❌ ALGUNO DE LOS TESTS FALLÓ ❌")

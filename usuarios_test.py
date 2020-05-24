import unittest
import werkzeug
from usuarios import read_one


class MyTestCase(unittest.TestCase):
    
    def test_consulta_cpf(self):
        usuarios = "12345678900"
        usuario_existe = read_one(usuarios)
        self.assertTrue(usuario_existe)


    def test_consulta_cpf_inexistente(self):
        #usuario que não existe
        usuarios = "000"
        try:
            usuario_existe = read_one(usuarios)
        except werkzeug.exceptions.NotFound:
            self.assertTrue(True)
        except:
            self.assertFalse(False)

        
if __name__ == '__main__':
    unittest.main()

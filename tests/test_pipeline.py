import unittest

from src.modelos import Pasajero
from src.pipeline import filtrar_grupo, resumir_grupo


def pasajero(id_, clase=1, edad=30.0, sobrevivio=True):
    """Arma una ficha de prueba con valores por defecto."""
    return Pasajero(id_, f"Apellido{id_}, Mr. Nombre", "12345", clase, edad, sobrevivio)


class TestResumirGrupo(unittest.TestCase):
    def test_dos_sobrevivientes_de_cuatro_da_0_5(self):
        grupo = [
            pasajero(1, sobrevivio=True),
            pasajero(2, sobrevivio=True),
            pasajero(3, sobrevivio=False),
            pasajero(4, sobrevivio=False),
        ]
        resumen = resumir_grupo(grupo)
        self.assertEqual(resumen["cantidad"], 4)
        self.assertEqual(resumen["sobrevivientes"], 2)
        self.assertEqual(resumen["proporcion"], 0.5)

    def test_grupo_vacio_no_divide_por_cero(self):
        resumen = resumir_grupo([])
        self.assertEqual(resumen["cantidad"], 0)
        self.assertIsNone(resumen["proporcion"])


class TestGrupoDeEdad(unittest.TestCase):
    def test_limite_entre_menor_y_adulto(self):
        self.assertEqual(pasajero(1, edad=17.9).grupo_edad(), "menor")
        self.assertEqual(pasajero(2, edad=18.0).grupo_edad(), "adulto")

    def test_edad_desconocida_no_entra_en_menor_ni_adulto(self):
        grupo = [pasajero(1, edad=10.0), pasajero(2, edad=40.0), pasajero(3, edad=None)]
        self.assertEqual(len(filtrar_grupo(grupo, grupo_edad="menor")), 1)
        self.assertEqual(len(filtrar_grupo(grupo, grupo_edad="adulto")), 1)
        self.assertEqual(len(filtrar_grupo(grupo, grupo_edad="desconocida")), 1)


if __name__ == "__main__":
    unittest.main()
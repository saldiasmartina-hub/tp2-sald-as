import unittest
from pathlib import Path

from src.fuentes import FuenteCSV
from src.modelos import Pasajero
from src.pipeline import filtrar_grupo, limpiar_pasajeros, resumir_grupo

DATOS = Path(__file__).resolve().parent.parent / "data"


def pasajero(id_, clase=1, edad=30.0, sobrevivio=True):
    """Arma una ficha de prueba con valores por defecto."""
    return Pasajero(id_, f"Apellido{id_}, Mr. Nombre", "12345", clase, edad, sobrevivio)


def fila(**cambios):
    """Una fila válida del CSV (todo texto); se le pueden cambiar campos."""
    base = {
        "PassengerId": "1",
        "Survived": "1",
        "Pclass": "3",
        "Name": "Allen, Mr. William",
        "Age": "22",
        "Ticket": "A/5 21171",
    }
    base.update(cambios)
    return base


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


class TestLimpieza(unittest.TestCase):
    def test_id_duplicado_se_rechaza_y_se_conserva_el_primero(self):
        registros = [fila(PassengerId="1"), fila(PassengerId="1", Pclass="1")]
        validos, rechazos = limpiar_pasajeros(registros)
        self.assertEqual(len(validos), 1)
        self.assertEqual(validos[0].clase, 3)
        self.assertEqual(rechazos, [("1", "PassengerId duplicado")])

    def test_fila_invalida_queda_en_rechazos_con_su_motivo(self):
        registros = [fila(PassengerId="1"), fila(PassengerId="2", Survived="9")]
        validos, rechazos = limpiar_pasajeros(registros)
        self.assertEqual(len(validos), 1)
        self.assertEqual(rechazos[0][0], "2")
        self.assertIn("Survived", rechazos[0][1])

    def test_edad_vacia_no_se_rechaza(self):
        validos, rechazos = limpiar_pasajeros([fila(Age="")])
        self.assertEqual(len(validos), 1)
        self.assertEqual(rechazos, [])
        self.assertIsNone(validos[0].edad)

    def test_se_conservan_las_cantidades_con_los_datos_reales(self):
        registros = FuenteCSV(DATOS / "titanic.csv").cargar()
        validos, rechazos = limpiar_pasajeros(registros)
        self.assertEqual(len(validos) + len(rechazos), len(registros))
        self.assertEqual(len(registros), 891)
        self.assertEqual(len(validos), 887)
        self.assertEqual(sorted(r[0] for r in rechazos), ["180", "272", "303", "598"])


if __name__ == "__main__":
    unittest.main()
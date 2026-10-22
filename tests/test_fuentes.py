import unittest
from pathlib import Path

from src.fuentes import ErrorDeLectura, FuenteCSV, FuenteJSON

DATOS = Path(__file__).resolve().parent.parent / "data"


class TestFuentes(unittest.TestCase):
    def test_csv_y_json_devuelven_los_mismos_registros(self):
        desde_csv = FuenteCSV(DATOS / "titanic.csv").cargar()
        desde_json = FuenteJSON(DATOS / "titanic.json").cargar()
        self.assertEqual(len(desde_csv), 891)
        self.assertEqual(desde_csv, desde_json)

    def test_csv_inexistente_falla_con_mensaje_claro(self):
        with self.assertRaises(ErrorDeLectura) as contexto:
            FuenteCSV(DATOS / "no_existe.csv").cargar()
        self.assertIn("No se encontró el archivo", str(contexto.exception))

    def test_json_inexistente_falla_con_mensaje_claro(self):
        with self.assertRaises(ErrorDeLectura):
            FuenteJSON(DATOS / "no_existe.json").cargar()


if __name__ == "__main__":
    unittest.main()
import unittest

from src.modelos import Pasajero
from src.validacion import (
    ErrorDeValidacion,
    convertir_edad,
    convertir_entero_en,
    validar_billete,
    validar_esquema,
)


def registro(**cambios):
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


class TestEdad(unittest.TestCase):
    def test_edad_valida_vacia_y_limites(self):
        self.assertEqual(convertir_edad("22"), 22.0)
        self.assertEqual(convertir_edad("0.42"), 0.42)
        self.assertEqual(convertir_edad("100"), 100.0)
        self.assertIsNone(convertir_edad(""))

    def test_edad_invalida_lanza_error(self):
        for texto in ("abc", "0", "-3", "150"):
            with self.subTest(texto=texto):
                with self.assertRaises(ErrorDeValidacion):
                    convertir_edad(texto)


class TestEnterosPermitidos(unittest.TestCase):
    def test_supervivencia_solo_0_o_1(self):
        self.assertEqual(convertir_entero_en("1", (0, 1), "Survived"), 1)
        with self.assertRaises(ErrorDeValidacion):
            convertir_entero_en("2", (0, 1), "Survived")

    def test_clase_solo_1_2_o_3(self):
        with self.assertRaises(ErrorDeValidacion):
            convertir_entero_en("4", (1, 2, 3), "Pclass")
        with self.assertRaises(ErrorDeValidacion):
            convertir_entero_en("x", (1, 2, 3), "Pclass")


class TestBilleteConRegex(unittest.TestCase):
    def test_billetes_con_formato_valido(self):
        for texto in ("113803", "PC 17599", "A/5 21171", "STON/O2. 3101282"):
            with self.subTest(texto=texto):
                self.assertEqual(validar_billete(texto), texto)

    def test_billetes_con_formato_invalido(self):
        for texto in ("LINE", "", "ABC", None):
            with self.subTest(texto=texto):
                with self.assertRaises(ErrorDeValidacion):
                    validar_billete(texto)


class TestEsquema(unittest.TestCase):
    def test_esquema_completo_no_lanza_error(self):
        validar_esquema([registro()])

    def test_sin_registros_lanza_error(self):
        with self.assertRaises(ErrorDeValidacion) as contexto:
            validar_esquema([])
        self.assertIn("no contiene registros", str(contexto.exception))

    def test_columnas_faltantes_se_nombran_en_el_mensaje(self):
        fila = registro()
        del fila["Survived"]
        del fila["Ticket"]
        with self.assertRaises(ErrorDeValidacion) as contexto:
            validar_esquema([fila])
        self.assertIn("Survived", str(contexto.exception))
        self.assertIn("Ticket", str(contexto.exception))


class TestPasajeroDesdeRegistro(unittest.TestCase):
    def test_convierte_los_tipos(self):
        p = Pasajero.desde_registro(registro())
        self.assertEqual(p.id_pasajero, 1)
        self.assertEqual(p.clase, 3)
        self.assertEqual(p.edad, 22.0)
        self.assertIs(p.sobrevivio, True)

    def test_edad_vacia_queda_como_none(self):
        self.assertIsNone(Pasajero.desde_registro(registro(Age="")).edad)

    def test_registro_invalido_lanza_error(self):
        with self.assertRaises(ErrorDeValidacion):
            Pasajero.desde_registro(registro(Survived="2"))
        with self.assertRaises(ErrorDeValidacion):
            Pasajero.desde_registro(registro(Ticket="LINE"))


if __name__ == "__main__":
    unittest.main()
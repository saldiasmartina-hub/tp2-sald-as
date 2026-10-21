from dataclasses import dataclass
from typing import Optional

from src.validacion import (
    ErrorDeValidacion,
    convertir_edad,
    convertir_entero_en,
    validar_billete,
)

EDAD_ADULTO = 18


@dataclass(frozen=True)
class Pasajero:
    """Ficha de un pasajero del Titanic."""

    id_pasajero: int
    nombre: str
    billete: str
    clase: int
    edad: Optional[float]
    sobrevivio: bool

    @classmethod
    def desde_registro(cls, registro):
        """Crea un Pasajero desde un diccionario de texto o lanza ErrorDeValidacion."""
        nombre = (registro.get("Name") or "").strip()
        if not nombre:
            raise ErrorDeValidacion("El nombre está vacío")
        return cls(
            id_pasajero=convertir_entero_en(
                registro.get("PassengerId"), range(1, 10**7), "PassengerId"
            ),
            nombre=nombre,
            billete=validar_billete(registro.get("Ticket")),
            clase=convertir_entero_en(registro.get("Pclass"), (1, 2, 3), "Pclass"),
            edad=convertir_edad(registro.get("Age")),
            sobrevivio=bool(convertir_entero_en(registro.get("Survived"), (0, 1), "Survived")),
        )

    def grupo_edad(self):
        """Devuelve 'menor', 'adulto' o 'desconocida'."""
        if self.edad is None:
            return "desconocida"
        if self.edad < EDAD_ADULTO:
            return "menor"
        return "adulto"
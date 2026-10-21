from dataclasses import dataclass
from typing import Optional

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

    def grupo_edad(self):
        """Devuelve 'menor', 'adulto' o 'desconocida'."""
        if self.edad is None:
            return "desconocida"
        if self.edad < EDAD_ADULTO:
            return "menor"
        return "adulto"
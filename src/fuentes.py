import csv
from abc import ABC, abstractmethod
from pathlib import Path


class ErrorDeLectura(Exception):
    """El archivo no existe o está mal formado."""


class FuenteDatos(ABC):
    """Contrato: toda fuente de datos sabe hacer cargar()."""

    def __init__(self, ruta):
        self._ruta = Path(ruta)

    @property
    def ruta(self):
        return self._ruta

    @abstractmethod
    def cargar(self):
        """Devuelve una lista de diccionarios, uno por pasajero."""


class FuenteCSV(FuenteDatos):
    def cargar(self):
        if not self.ruta.is_file():
            raise ErrorDeLectura(f"No se encontró el archivo: {self.ruta}")
        with open(self.ruta, newline="", encoding="utf-8") as archivo:
            return list(csv.DictReader(archivo))
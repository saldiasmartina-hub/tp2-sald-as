from src.modelos import Pasajero
from src.validacion import ErrorDeValidacion


def limpiar_pasajeros(registros):
    """Devuelve (pasajeros válidos, rechazos). Cada rechazo es (id, motivo)."""
    pasajeros = []
    rechazos = []
    ids_vistos = set()
    for numero, registro in enumerate(registros, start=2):  # la fila 1 es el encabezado
        id_texto = registro.get("PassengerId") or f"fila {numero}"
        try:
            pasajero = Pasajero.desde_registro(registro)
        except ErrorDeValidacion as error:
            rechazos.append((id_texto, str(error)))
            continue
        if pasajero.id_pasajero in ids_vistos:
            rechazos.append((id_texto, "PassengerId duplicado"))
            continue
        ids_vistos.add(pasajero.id_pasajero)
        pasajeros.append(pasajero)
    return pasajeros, rechazos
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


def indexar_pasajeros(pasajeros):
    """Devuelve un diccionario {id_pasajero: Pasajero} para buscar rápido."""
    return {p.id_pasajero: p for p in pasajeros}


def buscar_pasajero(indice, id_pasajero):
    """Devuelve la ficha del pasajero o None si el identificador no existe."""
    return indice.get(id_pasajero)


def filtrar_grupo(pasajeros, clase=None, grupo_edad=None):
    """Devuelve los pasajeros que cumplen los criterios indicados.

    Un criterio en None no filtra. Ejemplo: clase=1, grupo_edad="menor".
    """
    return [
        p
        for p in pasajeros
        if (clase is None or p.clase == clase)
        and (grupo_edad is None or p.grupo_edad() == grupo_edad)
    ]
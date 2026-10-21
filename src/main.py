"""Punto de entrada: explorador de pasajeros del Titanic."""
import argparse
import sys

from src.fuentes import ErrorDeLectura, FuenteCSV, FuenteJSON
from src.pipeline import buscar_pasajero, indexar_pasajeros, limpiar_pasajeros


def elegir_fuente(ruta):
    """Elige FuenteCSV o FuenteJSON según la extensión del archivo."""
    if ruta.lower().endswith(".csv"):
        return FuenteCSV(ruta)
    if ruta.lower().endswith(".json"):
        return FuenteJSON(ruta)
    raise ErrorDeLectura(f"Formato no soportado (use .csv o .json): {ruta}")


def construir_parser():
    parser = argparse.ArgumentParser(description="Explorador de pasajeros del Titanic.")
    parser.add_argument(
        "--entrada", default="data/titanic.csv", help="archivo .csv o .json con los datos"
    )
    subcomandos = parser.add_subparsers(dest="operacion", required=True)

    buscar = subcomandos.add_parser("buscar", help="mostrar la ficha de un pasajero")
    buscar.add_argument("--id", type=int, required=True, help="identificador del pasajero")
    return parser


def main(argv=None):
    args = construir_parser().parse_args(argv)
    try:
        registros = elegir_fuente(args.entrada).cargar()
    except ErrorDeLectura as error:
        print(f"Error de lectura: {error}", file=sys.stderr)
        return 1

    pasajeros, rechazos = limpiar_pasajeros(registros)

    if args.operacion == "buscar":
        ficha = buscar_pasajero(indexar_pasajeros(pasajeros), args.id)
        if ficha is None:
            print(f"No existe un pasajero válido con id {args.id}.")
            return 1
        print(f"Id: {ficha.id_pasajero}")
        print(f"Nombre: {ficha.nombre}")
        print(f"Billete: {ficha.billete}")
        print(f"Clase: {ficha.clase}")
        print(f"Edad: {ficha.edad if ficha.edad is not None else 'desconocida'}")
        print(f"Grupo de edad: {ficha.grupo_edad()}")
        print(f"Sobrevivió: {'sí' if ficha.sobrevivio else 'no'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
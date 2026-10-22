"""Punto de entrada: explorador de pasajeros del Titanic."""
import argparse
import sys

from src.fuentes import ErrorDeLectura, FuenteCSV, FuenteJSON
from src.pipeline import (
    buscar_pasajero,
    exportar_fichas,
    exportar_rechazos,
    filtrar_grupo,
    indexar_pasajeros,
    limpiar_pasajeros,
    resumir_grupo,
)
from src.validacion import ErrorDeValidacion, validar_esquema


def elegir_fuente(ruta):
    """Elige FuenteCSV o FuenteJSON según la extensión del archivo."""
    if ruta.lower().endswith(".csv"):
        return FuenteCSV(ruta)
    if ruta.lower().endswith(".json"):
        return FuenteJSON(ruta)
    raise ErrorDeLectura(f"Formato no soportado (use .csv o .json): {ruta}")


def agregar_filtros(subparser):
    """Agrega los filtros de grupo que comparten resumir y exportar."""
    subparser.add_argument("--clase", type=int, choices=(1, 2, 3), help="clase del pasaje")
    subparser.add_argument(
        "--grupo-edad",
        choices=("menor", "adulto", "desconocida"),
        help="grupo de edad",
    )


def construir_parser():
    parser = argparse.ArgumentParser(description="Explorador de pasajeros del Titanic.")
    parser.add_argument(
        "--entrada", default="data/titanic.csv", help="archivo .csv o .json con los datos"
    )
    parser.add_argument(
        "--rechazos",
        default="outputs/rechazos.csv",
        help="archivo CSV donde se guardan las filas rechazadas y su motivo",
    )
    subcomandos = parser.add_subparsers(dest="operacion", required=True)

    buscar = subcomandos.add_parser("buscar", help="mostrar la ficha de un pasajero")
    buscar.add_argument("--id", type=int, required=True, help="identificador del pasajero")

    resumir = subcomandos.add_parser("resumir", help="resumir un grupo de pasajeros")
    agregar_filtros(resumir)

    exportar = subcomandos.add_parser("exportar", help="guardar las fichas de un grupo en CSV")
    agregar_filtros(exportar)
    exportar.add_argument(
        "--salida", default="outputs/fichas.csv", help="archivo CSV de destino"
    )
    return parser


def main(argv=None):
    args = construir_parser().parse_args(argv)
    try:
        registros = elegir_fuente(args.entrada).cargar()
        validar_esquema(registros)
    except ErrorDeLectura as error:
        print(f"Error de lectura: {error}", file=sys.stderr)
        return 1
    except ErrorDeValidacion as error:
        print(f"Error en los datos: {error}", file=sys.stderr)
        return 1

    pasajeros, rechazos = limpiar_pasajeros(registros)
    exportar_rechazos(rechazos, args.rechazos)
    print(
        f"Limpieza: {len(registros)} filas leídas, {len(pasajeros)} válidas, "
        f"{len(rechazos)} rechazadas (detalle en {args.rechazos})"
    )
    print()

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

    elif args.operacion == "resumir":
        grupo = filtrar_grupo(pasajeros, clase=args.clase, grupo_edad=args.grupo_edad)
        resumen = resumir_grupo(grupo)
        print(f"Grupo: clase={args.clase or 'todas'}, edad={args.grupo_edad or 'todas'}")
        print(f"Pasajeros: {resumen['cantidad']}")
        print(f"Sobrevivientes: {resumen['sobrevivientes']}")
        if resumen["proporcion"] is None:
            print("Proporción: no se puede calcular (el grupo está vacío)")
        else:
            print(f"Proporción de sobrevivientes: {resumen['proporcion']}")

    elif args.operacion == "exportar":
        grupo = filtrar_grupo(pasajeros, clase=args.clase, grupo_edad=args.grupo_edad)
        if not grupo:
            print("El grupo está vacío: no se generó ningún archivo.")
            return 1
        escritas = exportar_fichas(grupo, args.salida)
        print(f"Se guardaron {escritas} fichas en {args.salida}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
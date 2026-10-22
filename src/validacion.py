import re

EDAD_MAXIMA = 100

# Columnas que el análisis necesita como mínimo.
COLUMNAS_REQUERIDAS = ("PassengerId", "Survived", "Pclass", "Name", "Age", "Ticket")

# Billete: palabras de prefijo opcionales (letras, números, puntos o barras)
# separadas por espacios, y al final un número. Ejemplos válidos:
# "113803", "PC 17599", "A/5 21171", "STON/O2. 3101282".
# La regex solo comprueba la FORMA, no que el billete exista.
PATRON_BILLETE = re.compile(r"(?:[A-Za-z0-9./]+ )*[0-9]+")


class ErrorDeValidacion(ValueError):
    """Un dato no cumple las condiciones necesarias para el análisis."""


def validar_esquema(registros):
    """Comprueba que haya registros y que estén todas las columnas necesarias."""
    if not registros:
        raise ErrorDeValidacion("El archivo no contiene registros")
    faltantes = [c for c in COLUMNAS_REQUERIDAS if c not in registros[0]]
    if faltantes:
        raise ErrorDeValidacion("Faltan columnas obligatorias: " + ", ".join(faltantes))


def convertir_edad(texto):
    """Convierte la edad a número. Si está vacía, devuelve None."""
    if texto is None or texto.strip() == "":
        return None
    try:
        edad = float(texto)
    except ValueError:
        raise ErrorDeValidacion(f"La edad no es un número: {texto!r}") from None
    if edad <= 0 or edad > EDAD_MAXIMA:
        raise ErrorDeValidacion(f"La edad está fuera de rango (0 a {EDAD_MAXIMA}): {edad}")
    return edad


def convertir_entero_en(texto, permitidos, nombre_campo):
    """Convierte a entero y comprueba que esté entre los valores permitidos."""
    try:
        numero = int(texto)
    except (TypeError, ValueError):
        raise ErrorDeValidacion(f"{nombre_campo} no es un entero: {texto!r}") from None
    if numero not in permitidos:
        raise ErrorDeValidacion(
            f"{nombre_campo} fuera de los valores permitidos {sorted(permitidos)}: {numero}"
        )
    return numero


def validar_billete(texto):
    """Devuelve el billete sin espacios sobrantes o lanza ErrorDeValidacion."""
    billete = (texto or "").strip()
    if PATRON_BILLETE.fullmatch(billete) is None:
        raise ErrorDeValidacion(f"El billete no tiene un formato válido: {texto!r}")
    return billete
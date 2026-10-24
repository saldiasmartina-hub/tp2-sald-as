# Datos

## Fuente

- **Conjunto:** Titanic (lista de pasajeros), 891 registros.
- **URL de obtención:**
  https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv
- **Responsable:** Data Science Dojo (repositorio de GitHub que publica la copia).
- **Licencia / condiciones de uso:** conjunto de uso público y educativo; la copia
  consultada no declara una licencia explícita.
- **Fecha de consulta:** 20/10/2026.
- **Archivos en este repositorio:** `data/titanic.csv` (copia sin modificar) y
  `data/titanic.json` (el mismo contenido en JSON, generado con
  `scripts/generar_json.py`).

## Unidad de análisis

Cada fila representa **un pasajero** del Titanic.

## Variables utilizadas

| Variable | Qué representa | Tipo |
|---|---|---|
| `PassengerId` | Identificador único del pasajero | entero |
| `Name` | Nombre del pasajero | texto |
| `Ticket` | Código del billete | texto |
| `Pclass` | Clase del pasaje (1, 2 o 3) | categórica |
| `Age` | Edad en años (puede faltar) | numérica |
| `Survived` | 1 = sobrevivió, 0 = no sobrevivió | 0/1 |

## Limitaciones

- La edad (`Age`) tiene valores faltantes. Esos pasajeros se clasifican como
  "edad desconocida" y no entran en la comparación menores/adultos.
- Es el registro de un único evento: los resultados describen a estos pasajeros
  y no se generalizan a otras situaciones.
- Las diferencias entre grupos son descriptivas, no explican causas.

## Unidad de análisis

Cada fila representa **un pasajero** del Titanic.

## Variables utilizadas

| Variable | Qué representa | Tipo |
|---|---|---|
| `PassengerId` | Identificador único del pasajero | entero |
| `Name` | Nombre del pasajero | texto |
| `Ticket` | Código del billete | texto |
| `Pclass` | Clase del pasaje (1, 2 o 3) | categórica |
| `Age` | Edad en años (puede faltar) | numérica |
| `Survived` | 1 = sobrevivió, 0 = no sobrevivió | 0/1 |

## Limitaciones

- La edad (`Age`) tiene valores faltantes. Esos pasajeros se clasifican como
  "edad desconocida" y no entran en la comparación menores/adultos.
- Es el registro de un único evento: los resultados describen a estos pasajeros
  y no se generalizan a otras situaciones.
- Las diferencias entre grupos son descriptivas, no explican causas.
- Cuatro filas (pasajeros 180, 272, 303 y 598) tienen el billete `LINE`, que no
  cumple el esquema de billete definido; se rechazan al limpiar y quedan registradas en `outputs/rechazos.csv`. 
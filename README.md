# TP2 – Supervivencia de menores y adultos en el Titanic

**Autora:** Martina Saldías
**Materia:** Programación Orientada a Datos – TP2 individual (2026)

## Problema, usuario y pregunta

- **Problema:** en el hundimiento del Titanic no todos los pasajeros tuvieron la
  misma probabilidad de sobrevivir. Se quiere describir si la edad (menor o
  adulto) marcó una diferencia en la proporción de sobrevivientes y si esa
  diferencia cambia según la clase del pasaje.
- **Usuario:** una persona que quiere explorar el conjunto de datos del Titanic
  (por ejemplo, estudiantes de ciencia de datos) y necesita además saber qué
  registros se descartaron y por qué.
- **Pregunta guía:** ¿los menores de 18 años sobrevivieron más que los adultos
  dentro de cada clase?
- **Resultado:** una tabla con una fila por clase (1.ª, 2.ª, 3.ª) y grupo de edad
  (menor, adulto), con la cantidad de pasajeros, la cantidad de sobrevivientes
  y la tasa de supervivencia. Se interpreta como una **comparación descriptiva
  de proporciones**, no como una explicación de causas.
- **Definición:** "menor" es una persona con edad menor a 18 años;
  "adulto", con 18 años o más.

## Alcance de la primera versión

- **Incluye:**
  - lectura de los datos desde archivos CSV y JSON;
  - validación y limpieza, con un informe de los registros rechazados;
  - cálculo de la tasa de supervivencia por clase y grupo de edad;
  - guardado de la tabla en un archivo de salida.
- **No incluye:** modelos predictivos, pruebas estadísticas, gráficos, aplicación

## Solución propuesta y operaciones

Un explorador de consola que permite trabajar con la lista de pasajeros del
Titanic. Quien lo use puede:

- **Buscar** un pasajero por su identificador y ver su ficha.
- **Filtrar** un grupo por clase (1.ª, 2.ª, 3.ª) y grupo de edad (menor,
  adulto o edad desconocida).
- **Resumir** el grupo filtrado: cantidad de pasajeros, cantidad de
  sobrevivientes y proporción de supervivencia.
- **Exportar** las fichas y el resumen del grupo seleccionado a un archivo.

La pregunta guía se responde comparando el resumen de los menores con el de
los adultos dentro de cada clase.
  web ni el uso de las columnas `SibSp`, `Parch`, `Ticket` y `Embarked`.
- **Decisión sobre datos faltantes:** los pasajeros sin edad no se descartan del
  conjunto; solo se excluyen de esta comparación y se informa cuántos son.

## Solución propuesta y operaciones

Un explorador de consola que permite trabajar con la lista de pasajeros del
Titanic. Quien lo use puede:

- **Buscar** un pasajero por su identificador y ver su ficha.
- **Filtrar** un grupo por clase (1.ª, 2.ª, 3.ª) y grupo de edad (menor,
  adulto o edad desconocida).
- **Resumir** el grupo filtrado: cantidad de pasajeros, cantidad de
  sobrevivientes y proporción de supervivencia.
- **Exportar** las fichas y el resumen del grupo seleccionado a un archivo.

La pregunta guía se responde comparando el resumen de los menores con el de
los adultos dentro de cada clase.

## Instalación y ejecución

Requiere **Python 3.10 o superior**. No hay dependencias externas: solo se usa la
biblioteca estándar (`requirements.txt` lo aclara).

```bash
git clone https://github.com/saldiasmartina-hub/tp2-sald-as.git
cd tp2-sald-as
```

> En Windows, si el comando `python` no funciona, usar `py` en su lugar.

### Operaciones

Buscar la ficha de un pasajero por su identificador:

```bash
python -m src.main buscar --id 6
```

Resumir un grupo (cantidad, sobrevivientes y proporción). Los filtros
`--clase` (1, 2 o 3) y `--grupo-edad` (`menor`, `adulto` o `desconocida`) son opcionales:

```bash
python -m src.main resumir --clase 1 --grupo-edad menor
```

Exportar las fichas de un grupo a un archivo CSV:

```bash
python -m src.main exportar --clase 1 --grupo-edad menor --salida outputs/menores_clase1.csv
```

Todas las operaciones leen `data/titanic.csv` por defecto. Para leer el JSON
equivalente:

```bash
python -m src.main --entrada data/titanic.json resumir --clase 1
```

### Pruebas

```bash
python -m unittest discover -s tests -t . -v
```


## Organización del código

```
tp2-sald-as/
├── README.md
├── requirements.txt
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── main.py          # consola: elige la operación y muestra el resultado
│   ├── fuentes.py       # FuenteDatos (abstracta), FuenteCSV y FuenteJSON
│   ├── modelos.py       # clase Pasajero
│   ├── validacion.py    # conversiones, rangos y expresión regular del billete
│   └── pipeline.py      # limpieza, búsqueda, filtro, resumen y exportación
├── tests/               # pruebas con unittest
├── data/                # titanic.csv, titanic.json y README de los datos
├── scripts/
│   └── generar_json.py  # genera titanic.json a partir de titanic.csv
└── outputs/             # archivos exportados (no se versionan)
```

### Flujo de procesamiento

`leer` (`fuentes.py`) → `validar y limpiar` (`validacion.py`, `modelos.py`,
`pipeline.limpiar_pasajeros`) → `operar` (`buscar`, `filtrar`, `resumir`) →
`comunicar` (`main.py` muestra el resultado o `exportar_fichas` lo guarda).

### Responsabilidad de cada pieza

| Pieza | Responsabilidad |
|---|---|
| `FuenteDatos` | Contrato común: toda fuente sabe hacer `cargar()` |
| `FuenteCSV`, `FuenteJSON` | Leen su formato y devuelven la misma lista de diccionarios |
| `Pasajero` | Ficha con tipos correctos; calcula su grupo de edad |
| `convertir_edad`, `convertir_entero_en`, `validar_billete` | Validan un dato y lanzan `ErrorDeValidacion` con un mensaje claro |
| `limpiar_pasajeros` | Convierte las filas, aparta las rechazadas con su motivo y detecta duplicados |
| `indexar_pasajeros`, `buscar_pasajero` | Búsqueda por identificador |
| `filtrar_grupo`, `resumir_grupo` | Filtro por clase y grupo de edad; cantidad, sobrevivientes y proporción |
| `exportar_fichas` | Guarda un grupo en un archivo CSV |


## Decisiones de limpieza

Cada fila del archivo se valida al convertirla en un `Pasajero`. Las filas que no
cumplen no se pierden: quedan en la lista de rechazos con su identificador y el motivo.

| Situación | Decisión | Por qué |
|---|---|---|
| `PassengerId` repetido | Se conserva la primera aparición y se rechazan las demás | No se puede saber cuál es la correcta; elegir una al azar escondería el problema |
| `Survived` distinto de 0 o 1 | Se rechaza la fila | El resultado a analizar no es interpretable |
| `Pclass` distinta de 1, 2 o 3 | Se rechaza la fila | La clase define los grupos de comparación |
| `Age` no numérica, menor o igual a 0, o mayor a 100 | Se rechaza la fila | Es un valor imposible |
| `Age` vacía | **Se acepta** y el pasajero queda con edad desconocida | Es un faltante frecuente; descartarlo reduciría mucho los datos |
| `Ticket` sin formato válido | Se rechaza la fila | No cumple el esquema de billete definido (ver abajo) |
| `Name` vacío | Se rechaza la fila | La ficha del pasajero lo necesita |

### Qué valida la expresión regular del billete

El patrón `(?:[A-Za-z0-9./]+ )*[0-9]+` comprueba la **forma** del billete: cero o más
palabras de prefijo (letras, números, puntos o barras) seguidas de un espacio, y al
final un número. Acepta `113803`, `PC 17599`, `A/5 21171` o `STON/O2. 3101282`.
Se usa `fullmatch`, de modo que debe cumplirse en **todo** el texto. La regex solo
revisa la forma: no sabe si el billete existió realmente.

### Resultado de la limpieza sobre `data/titanic.csv`

| | Cantidad |
|---|---|
| Filas leídas | 891 |
| Pasajeros válidos | 887 |
| Filas rechazadas | 4 |
| Válidos sin edad (grupo "desconocida") | 177 |

Las 4 filas rechazadas (pasajeros 180, 272, 303 y 598) tienen el billete `LINE`, que
no termina en número y por lo tanto no cumple el esquema. En este archivo no se
encontraron identificadores repetidos ni valores fuera de rango.


## Ejemplo de resultado

Pregunta guía: ¿los menores de 18 años sobrevivieron más que los adultos dentro de cada
clase? Se obtiene ejecutando `resumir` una vez por grupo, por ejemplo:

```bash
python -m src.main resumir --clase 2 --grupo-edad menor
```

```
Grupo: clase=2, edad=menor
Pasajeros: 23
Sobrevivientes: 21
Proporción de sobrevivientes: 0.913
```

Resultados sobre `data/titanic.csv` (887 pasajeros válidos):

| Clase | Grupo de edad | Pasajeros | Sobrevivientes | Proporción |
|---|---|---|---|---|
| 1 | menor | 12 | 11 | 0.917 |
| 1 | adulto | 174 | 111 | 0.638 |
| 2 | menor | 23 | 21 | 0.913 |
| 2 | adulto | 150 | 62 | 0.413 |
| 3 | menor | 78 | 29 | 0.372 |
| 3 | adulto | 273 | 55 | 0.201 |

Los 177 pasajeros válidos sin edad quedan fuera de esta comparación (grupo "desconocida").


## Interpretación y limitaciones

### Qué muestran los resultados

En esta copia del conjunto, los menores de 18 años tuvieron una proporción de
sobrevivientes mayor que los adultos **en las tres clases**:

| Clase | Menores | Adultos | Diferencia |
|---|---|---|---|
| 1 | 0.917 | 0.638 | 0.279 |
| 2 | 0.913 | 0.413 | 0.500 |
| 3 | 0.372 | 0.201 | 0.171 |

La diferencia es la más grande en 2.ª clase y la más chica en 3.ª. En 3.ª clase,
además, la proporción de los menores (0.372) es mucho menor que en las otras dos.

### Qué NO se puede concluir

- **No es una explicación de causas.** Los resultados describen a estos pasajeros.
  La edad está relacionada con otras variables que no se analizan aquí (sexo,
  ubicación en el barco, tamaño de la familia), por lo que no se puede afirmar que
  ser menor haya sido la causa de sobrevivir.
- **No se generalizan** a otros naufragios ni a otras poblaciones.

### Limitaciones de los datos y del análisis

- **Grupos chicos:** hay solo 12 menores en 1.ª clase y 23 en 2.ª. Una proporción
  calculada sobre tan pocos casos es poco estable: unas pocas personas más o menos
  cambiarían bastante el valor.
- **Edades faltantes:** 177 de los 887 pasajeros válidos (cerca del 20 %) no tienen
  edad y quedan fuera de la comparación. Como no se sabe por qué faltan, el resultado
  podría cambiar si se conocieran.
- **Filas rechazadas por el billete:** se descartaron 4 pasajeros por tener el
  billete `LINE`, que no cumple el esquema definido. Es una decisión de diseño, y
  son pocos casos, pero es información que se pierde.
- **Definición de "menor":** se usó el corte de 18 años; con otro corte los números
  cambiarían.
- **Alcance de la fuente:** la copia usada no declara una licencia explícita y no es
  una lista oficial completa de las personas a bordo.


## Datos

- **Fuente:** lista de pasajeros del Titanic, copia en CSV publicada en el repositorio
  `datasciencedojo/datasets` de GitHub.
- **URL:** https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv
- **Responsable:** Data Science Dojo (quien publica la copia).
- **Licencia / condiciones de uso:** conjunto de uso público y educativo; la copia
  consultada **no declara una licencia explícita**.
- **Fecha de consulta:** 20/10/2026.
- **Unidad de análisis:** cada fila representa **un pasajero**.
- **Tamaño:** 891 registros y 12 columnas; el análisis usa `PassengerId`, `Name`,
  `Ticket`, `Pclass`, `Age` y `Survived`.
- **Archivos:** `data/titanic.csv` y su equivalente `data/titanic.json`, generado con
  `scripts/generar_json.py`.

El detalle de cada variable y las limitaciones de los datos están en
[`data/README.md`](data/README.md).
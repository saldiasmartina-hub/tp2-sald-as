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


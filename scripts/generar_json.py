"""Convierte data/titanic.csv en data/titanic.json (lista de objetos)."""
import csv
import json

with open("data/titanic.csv", newline="", encoding="utf-8") as archivo:
    filas = list(csv.DictReader(archivo))

with open("data/titanic.json", "w", encoding="utf-8") as salida:
    json.dump(filas, salida, ensure_ascii=False, indent=1)

print(f"Se escribieron {len(filas)} registros en data/titanic.json")
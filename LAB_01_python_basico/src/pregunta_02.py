def pregunta_02():
    """
    Cuente cuántos registros hay para cada letra de la primera columna
    (`letter`). Retorne una lista de tuplas `(letra, cantidad)` ordenada
    alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 8), ("B", 7), ("C", 5), ...]
    """
    import csv
    import gzip
    from pathlib import Path

    ruta_datos = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"
    with gzip.open(ruta_datos, "rt", encoding="utf-8", newline="") as archivo:
            lector = csv.reader(archivo, delimiter="\t")
            diccionario_conteo = {}

            for registro in lector:
                letra = registro[0]
                diccionario_conteo[letra] = diccionario_conteo.get(letra, 0) + 1

            return sorted(diccionario_conteo.items())
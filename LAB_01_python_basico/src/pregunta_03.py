def pregunta_03():
    """
    Sume los valores de la segunda columna (`value`) para cada letra de la
    primera columna (`letter`). Retorne una lista de tuplas `(letra, suma)`
    ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 53), ("B", 36), ("C", 27), ...]
    """
    import csv
    import gzip

    with gzip.open("LAB_01_python_basico/data/data.csv.gz", "rt", encoding="utf-8", newline="") as archivo:
            lector = csv.reader(archivo, delimiter="\t")
            diccionario_conteo = {}

            for registro in lector:
                letra = registro[0]
                diccionario_conteo[letra] = diccionario_conteo.get(letra, 0) + int(registro[1])

            return sorted(diccionario_conteo.items())

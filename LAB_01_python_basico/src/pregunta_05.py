def pregunta_05():
    """
    Para cada letra de la primera columna (`letter`), encuentre el valor
    máximo y el valor mínimo de la segunda columna (`value`). Retorne una lista
    de tuplas `(letra, máximo, mínimo)` ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 9, 2), ("B", 9, 1), ...]
    """
    import csv
    import gzip

    with gzip.open("LAB_01_python_basico/data/data.csv.gz", "rt", encoding="utf-8", newline="") as archivo:
            lector = csv.reader(archivo, delimiter="\t")
            diccionario_conteo = {}

            for registro in lector:
                letra = registro[0]
                if letra in diccionario_conteo:
                    diccionario_conteo[letra] = (
                         max(diccionario_conteo.get(letra)[0], int(registro[1])), 
                         min(diccionario_conteo.get(letra)[1], int(registro[1]))
                         )
                else:
                     diccionario_conteo[letra] = (int(registro[1]), int(registro[1]))

            return sorted(diccionario_conteo.items())

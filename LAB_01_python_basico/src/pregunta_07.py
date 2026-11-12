def pregunta_07():
    """
    Para cada valor distinto de la segunda columna (`value`), construya la
    lista de letras de la primera columna (`letter`) que aparecen con ese
    valor. Conserve las letras repetidas y el orden en que aparecen en el
    archivo. Retorne una lista de tuplas `(valor, letras)` ordenada por el
    valor.

    Ejemplo del formato de la respuesta:

        [(0, ["C"]), (1, ["E", "B", "E"]), (2, ["A", "E"]), ...]
    """
    import csv
    import gzip

    with gzip.open("LAB_01_python_basico/data/data.csv.gz", "rt", encoding="utf-8", newline="") as archivo:
        lector = csv.reader(archivo, delimiter="\t")

        tuplas = [(registro[0], int(registro[1])) for registro in list(lector)]

        formato = [(valor, []) for _, valor in dict.fromkeys(tuplas)]
        return formato


print(pregunta_07())

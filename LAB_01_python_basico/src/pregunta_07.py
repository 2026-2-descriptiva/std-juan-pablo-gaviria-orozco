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
    from pathlib import Path

    ruta_datos = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"
    with gzip.open(ruta_datos, "rt", encoding="utf-8", newline="") as archivo:
        lector = csv.reader(archivo, delimiter="\t")

        tuplas = [(registro[0], int(registro[1])) for registro in list(lector)]
        
        diccionario_conteo = {numero:[] for _, numero in tuplas}

        for letra, valor in tuplas:
            diccionario_conteo[valor].append(letra)

        return sorted(diccionario_conteo.items())

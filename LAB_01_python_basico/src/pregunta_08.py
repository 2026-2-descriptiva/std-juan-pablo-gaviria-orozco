def pregunta_08():
    """
    Repita la pregunta 7, pero ahora cada lista de letras debe contener cada
    letra una sola vez y estar ordenada alfabéticamente. Retorne una lista de
    tuplas `(valor, letras)` ordenada por el valor.

    Ejemplo del formato de la respuesta:

        [(0, ["C"]), (1, ["B", "E"]), (2, ["A", "E"]), ...]
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
            if letra not in diccionario_conteo[valor]:
                diccionario_conteo[valor].append(letra)

        return [(valor, sorted(lista)) for valor, lista in sorted(list(diccionario_conteo.items()))]

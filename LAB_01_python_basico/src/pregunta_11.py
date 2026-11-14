def pregunta_11():
    """
    La cuarta columna (`codes`) contiene letras minúsculas separadas por
    comas. Para cada una de esas letras, sume los valores de la segunda
    columna (`value`) de los registros en los que aparece. Retorne un
    diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"a": 122, "b": 49, "c": 91, ...}
    """
    import csv
    import gzip
    from pathlib import Path

    ruta_datos = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"
    with gzip.open(ruta_datos, "rt", encoding="utf-8", newline="") as archivo:
        lector = csv.reader(archivo, delimiter="\t")

        columnas_necesarias = [(int(registro[1]), registro[3].split(",")) for registro in list(lector)]

        diccionario_conteos = {}

        for valor, letras in columnas_necesarias:
            for letra in letras:
                diccionario_conteos[letra] = diccionario_conteos.get(letra, 0) + valor

        return dict(sorted(list(diccionario_conteos.items())))
def pregunta_06():
    """
    La quinta columna (`metrics`) contiene pares `clave:valor` separados por
    comas. Para cada clave, encuentre el valor mínimo y el valor máximo que
    aparecen en todo el archivo. Retorne una lista de tuplas
    `(clave, mínimo, máximo)` ordenada alfabéticamente por la clave.

    Observe que el orden es mínimo y luego máximo, al contrario de la
    pregunta 5.

    Ejemplo del formato de la respuesta:

        [("aaa", 1, 9), ("bbb", 1, 9), ...]
    """
    import csv
    import gzip

    with gzip.open("LAB_01_python_basico/data/data.csv.gz", "rt", encoding="utf-8", newline="") as archivo:
        lector = csv.reader(archivo, delimiter="\t")
        limpieza_1 = [registro[4].split(",") for registro in list(lector)]
        limpieza_2 = [
                registro.split(":")
                for lista in limpieza_1
                for registro in lista
            ]
        diccionario_conteo = {
            key:(int(max(limpieza_2, key=lambda par: int(par[1]))[1]), 0) for key, _ in sorted(limpieza_2)
            }

        for key, value in limpieza_2:
            value = int(value)
            diccionario_conteo[key] = (
                min(diccionario_conteo[key][0], value),
                max(diccionario_conteo[key][1], value)
                                        )
        
        return [(registro[0], registro[1][0], registro[1][1]) for registro in diccionario_conteo.items()]


print(pregunta_06())



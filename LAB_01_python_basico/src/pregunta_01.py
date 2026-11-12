def pregunta_01():
    """
    Calcule la suma de los valores de la segunda columna (`value`) del
    archivo `data/data.csv.gz` y retorne el resultado como un número entero.

    Ejemplo del formato de la respuesta:

        214
    """
    import csv
    import gzip

    with gzip.open("LAB_01_python_basico/data/data.csv.gz", "rt", encoding="utf-8", newline="") as archivo:
        lector = csv.reader(archivo, delimiter="\t")
        total = 0
        for fila in lector:
            total += int(fila[1])

    return total
    

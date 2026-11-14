def pregunta_09():
    """
    Cuente cuántas veces aparece cada clave en la quinta columna (`metrics`)
    de todo el archivo. Retorne un diccionario `{clave: cantidad}` con las
    claves en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"aaa": 13, "bbb": 16, "ccc": 23, ...}
    """
    import csv
    import gzip
    from pathlib import Path

    ruta_datos = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"
    with gzip.open(ruta_datos, "rt", encoding="utf-8", newline="") as archivo:
        lector = csv.reader(archivo, delimiter="\t")

        metrics = [registro[4].split(",") for registro in list(lector)]

        claves_metrics = [par.split(":")[0] for registro in metrics for par in registro]

        diccionario_conteo = {clave:claves_metrics.count(clave) for clave in sorted(list(set(claves_metrics)))}

        return diccionario_conteo
def pregunta_12():
    """
    Para cada letra de la primera columna (`letter`), sume todos los valores
    numéricos de los pares `clave:valor` de la quinta columna (`metrics`).
    Retorne un diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"A": 177, "B": 187, "C": 114, ...}
    """
    import csv
    import gzip
    from pathlib import Path

    ruta_datos = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"
    with gzip.open(ruta_datos, "rt", encoding="utf-8", newline="") as archivo:
        lector = csv.reader(archivo, delimiter="\t")

        totales = {}

        for letra, _, _, _, lista in lector:
            suma_fila = sum(
                int(par.split(":", 1)[1])
                for par in lista.split(",")
            )
            totales[letra] = totales.get(letra, 0) + suma_fila

        resultado = dict(sorted(totales.items()))
        
        return resultado

print(pregunta_12())
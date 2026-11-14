def pregunta_06():
    """
    Usando `data/tbl1.tsv`, obtenga los valores distintos de la columna `c4`,
    conviértalos a mayúsculas y retórnelos como una lista ordenada
    alfabéticamente.

    Ejemplo del formato de la respuesta:

        ["A", "B", "C", "D", "E", "F", "G"]
    """

    from pathlib import Path

    import pandas as pd

    ruta = Path(__file__).resolve().parents[1] / "data" / "tbl1.tsv"
    tabla = pd.read_csv(ruta, sep="\t")
    return sorted(tabla["c4"].str.upper().unique().tolist())

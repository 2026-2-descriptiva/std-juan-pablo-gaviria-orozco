def main():
    """
    Antes de limpiar o analizar un conjunto de datos, un analista debe
    documentar qué problemas tiene. En este laboratorio usted no va a limpiar
    `data/ventas.csv.gz`: va a construir un reporte de calidad que deje evidencia
    de sus problemas, tal como están en el archivo.

    Lea `data/ventas.csv.gz` sin modificar sus valores. Para trabajar con los
    encabezados, normalícelos: páselos a minúsculas, elimine los espacios al
    inicio y al final (y cualquier marca BOM) y reemplace los espacios
    internos por `_`. Las columnas requeridas son `supplier_id`, `supplier`,
    `country`, `city`, `purchase_date`, `amount`, `discount`, `weight`,
    `units`, `unit_price` y `contact_email`.

    Escriba el reporte en `submission/data_quality_report.json` con estas
    claves:

    - `row_count`: cantidad de filas de datos.
    - `column_count`: cantidad de columnas.
    - `missing_required_columns`: lista ordenada de columnas requeridas que no
      están en el archivo.
    - `unexpected_columns`: lista ordenada de columnas del archivo que no son
      requeridas.
    - `duplicate_row_count`: cantidad de filas idénticas a una fila anterior.
    - `duplicate_supplier_id_row_count`: cantidad de filas cuyo `supplier_id`
      aparece más de una vez (cuente todas esas filas, no solo las
      repetidas).
    - `missing_value_count_by_column`: diccionario con la cantidad de valores
      faltantes de cada columna. Considere faltantes las celdas vacías y las
      que contienen `N/A`.
    - `invalid_email_count`: cantidad de valores de `contact_email` que no
      tienen la forma `usuario@dominio.extension`.
    - `invalid_unit_count`: cantidad de valores numéricos de `units` que no son
      enteros positivos. Los valores faltantes no se cuentan aquí.
    - `country_values`: lista ordenada de los valores distintos de `country`,
      escritos exactamente como aparecen en el archivo.

    La función también debe retornar el reporte como un diccionario.

    Ejemplo del formato del reporte:

        {
          "row_count": 103,
          "column_count": 11,
          "missing_required_columns": [],
          ...
          "country_values": [" Colombia ", "CO", ...]
        }
    """

    import json
    import re
    from pathlib import Path

    import pandas as pd

    directorio = Path(__file__).resolve().parents[1]
    ruta_datos = directorio / "data" / "ventas.csv.gz"
    tabla = pd.read_csv(
        ruta_datos,
        compression="gzip",
        dtype=str,
        keep_default_na=False,
        encoding="utf-8",
    )
    tabla.columns = (
        tabla.columns.str.replace("\ufeff", "", regex=False)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )

    columnas_requeridas = [
        "supplier_id",
        "supplier",
        "country",
        "city",
        "purchase_date",
        "amount",
        "discount",
        "weight",
        "units",
        "unit_price",
        "contact_email",
    ]
    faltantes = tabla.isin(["", "N/A"])
    unidades_faltantes = faltantes["units"]
    unidades = pd.to_numeric(tabla["units"].mask(unidades_faltantes), errors="coerce")
    unidades_invalidas = (
        ~unidades_faltantes
        & (
            unidades.isna()
            | (unidades <= 0)
            | (unidades % 1 != 0)
        )
    )
    correos_validos = tabla["contact_email"].str.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+")

    reporte = {
        "row_count": int(len(tabla)),
        "column_count": int(len(tabla.columns)),
        "missing_required_columns": sorted(
            set(columnas_requeridas) - set(tabla.columns)
        ),
        "unexpected_columns": sorted(
            set(tabla.columns) - set(columnas_requeridas)
        ),
        "duplicate_row_count": int(tabla.duplicated().sum()),
        "duplicate_supplier_id_row_count": int(
            tabla["supplier_id"].duplicated(keep=False).sum()
        ),
        "missing_value_count_by_column": {
            columna: int(faltantes[columna].sum()) for columna in tabla.columns
        },
        "invalid_email_count": int((~correos_validos).sum()),
        "invalid_unit_count": int(unidades_invalidas.sum()),
        "country_values": sorted(tabla["country"].unique().tolist()),
    }

    directorio_salida = directorio / "submission"
    directorio_salida.mkdir(parents=True, exist_ok=True)
    (directorio_salida / "data_quality_report.json").write_text(
        json.dumps(reporte, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return reporte

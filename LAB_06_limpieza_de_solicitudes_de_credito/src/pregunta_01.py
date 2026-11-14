def pregunta_01():
    """
    El archivo `data/solicitudes_de_credito.csv.gz` contiene las solicitudes de
    un programa de crédito, pero llegó sucio: tiene una columna de índice que
    no pertenece a los datos, registros duplicados, registros incompletos y
    valores que representan lo mismo escritos de formas distintas en los
    campos de texto, las fechas, el estrato y el monto.

    Su tarea es limpiarlo y guardar el resultado en
    `submission/solicitudes_de_credito.csv`, usando punto y coma (`;`) como
    separador y sin el índice de Pandas.

    El archivo limpio debe cumplir lo siguiente:

    - Contiene solamente las nueve columnas `sexo`, `tipo_de_emprendimiento`,
      `idea_negocio`, `barrio`, `estrato`, `comuna_ciudadano`,
      `fecha_de_beneficio`, `monto_del_credito` y `línea_credito`, en ese
      orden.
    - Los campos de texto están en minúsculas y sus palabras separadas por
      espacios.
    - `estrato` y `monto_del_credito` son números enteros, sin símbolos ni
      separadores de miles.
    - Todas las fechas de `fecha_de_beneficio` usan un mismo formato, por
      ejemplo `AAAA-MM-DD`.
    - No hay registros incompletos. La única excepción es
      `comuna_ciudadano`: sus valores faltantes son parte de los datos
      originales y deben conservarse.
    - No hay registros duplicados.

    Ejemplo del formato del archivo:

        sexo;tipo_de_emprendimiento;idea_negocio;barrio;estrato;...
        femenino;comercio;almacen de ropa en;los cerros el vergel;2;...
        ...
    """

    from pathlib import Path

    import pandas as pd

    directorio = Path(__file__).resolve().parents[1]
    ruta_datos = directorio / "data" / "solicitudes_de_credito.csv.gz"
    tabla = pd.read_csv(
        ruta_datos,
        sep=";",
        compression="gzip",
        dtype=str,
        keep_default_na=False,
        encoding="utf-8",
    ).iloc[:, 1:]
    tabla.columns = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "estrato",
        "comuna_ciudadano",
        "fecha_de_beneficio",
        "monto_del_credito",
        "línea_credito",
    ]

    columnas_texto = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "línea_credito",
    ]
    for columna in columnas_texto:
        tabla[columna] = (
            tabla[columna]
            .str.lower()
            .str.replace("-", " ", regex=False)
            .str.split()
            .str.join(" ")
        )

    columnas_requeridas = [columna for columna in tabla.columns if columna != "comuna_ciudadano"]
    tabla = tabla[tabla[columnas_requeridas].ne("").all(axis=1)].copy()

    tabla["estrato"] = pd.to_numeric(tabla["estrato"]).astype(int)
    tabla["comuna_ciudadano"] = pd.to_numeric(
        tabla["comuna_ciudadano"], errors="coerce"
    )
    tabla["monto_del_credito"] = pd.to_numeric(
        tabla["monto_del_credito"]
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
    ).astype(int)

    fechas = pd.to_datetime(
        tabla["fecha_de_beneficio"], format="%d/%m/%Y", errors="coerce"
    )
    for formato in ("%Y-%m-%d", "%Y/%m/%d"):
        fechas = fechas.fillna(
            pd.to_datetime(tabla["fecha_de_beneficio"], format=formato, errors="coerce")
        )
    tabla["fecha_de_beneficio"] = fechas.dt.strftime("%Y-%m-%d")
    tabla = tabla.drop_duplicates()

    directorio_salida = directorio / "submission"
    directorio_salida.mkdir(parents=True, exist_ok=True)
    tabla.to_csv(
        directorio_salida / "solicitudes_de_credito.csv",
        sep=";",
        index=False,
    )

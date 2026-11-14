import pandas as pd


def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Una entidad pública recibe peticiones, quejas, reclamos y sugerencias
    (PQRS) por dos canales, la página web y las cartas, y la ley le da 15 días
    hábiles para responder cada una. Su tarea es medir si la entidad cumple
    ese plazo.

    Los archivos `data/historical_requests_web.csv.gz` y
    `data/historical_requests_letter.csv.gz` tienen una fila por solicitud
    recibida entre 2016 y 2021 por cada canal, con su identificador
    (`record_id`), la fecha de entrada (`in_date`), el día de la semana de
    entrada (`day_name`) y la fecha de respuesta (`out_date`). Si `out_date`
    está vacía, la solicitud todavía no ha sido respondida.

    Tenga en cuenta lo siguiente:

    - Algunas solicitudes aparecen repetidas: elimine las filas idénticas
      dentro de cada canal, para contar cada solicitud una sola vez. Las
      filas sin `record_id` son solicitudes válidas.
    - Llame `letter` al canal de las cartas y `web` al de la página web.
    - Los días hábiles de respuesta son los días de lunes a viernes
      posteriores a la fecha de entrada, hasta la fecha de respuesta
      incluida. Por ejemplo, una solicitud que entra un viernes y se responde
      el lunes siguiente tardó 1 día hábil. No considere los festivos.
    - Los días calendario de respuesta son la diferencia entre la fecha de
      respuesta y la de entrada.
    - Una solicitud cumple el plazo si fue respondida en 15 días hábiles o
      menos. Una solicitud pendiente no ha cumplido el plazo.
    - `on_time_rate` es la proporción de solicitudes que cumplen el plazo,
      sobre el total de solicitudes, incluidas las pendientes.
    - Las medianas de días se calculan solamente con las solicitudes
      respondidas.

    Genere tres archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `channel_summary.csv`, con una fila por canal, en orden alfabético:
       `channel`, `requests`, `answered`, `pending`,
       `median_business_days` y `on_time_rate`.

    2. `yearly_summary.csv`, con una fila por año de entrada y canal,
       ordenada por año y luego por canal: `year`, `channel`, `requests`,
       `pending` y `on_time_rate`.

    3. `entry_day_summary.csv`, con una fila por día de entrada, de lunes a
       domingo, con los dos canales juntos: `day_name`, `requests`,
       `median_calendar_days` y `median_business_days`.

    Observe en el tercer archivo cómo cambia la lectura del tiempo de
    respuesta según se cuenten días calendario o días hábiles.

    La función también debe retornar las tres tablas, en el mismo orden.

    Ejemplo del formato de `channel_summary.csv`:

        channel,requests,answered,pending,median_business_days,on_time_rate
        letter,28138,...
        ...
    """

    from pathlib import Path

    import numpy as np

    directorio = Path(__file__).resolve().parents[1]
    datos_por_canal = []

    for canal in ("letter", "web"):
        nombre_archivo = (
            "historical_requests_letter.csv.gz"
            if canal == "letter"
            else "historical_requests_web.csv.gz"
        )
        datos_canal = pd.read_csv(
            directorio / "data" / nombre_archivo,
            compression="gzip",
            parse_dates=["in_date", "out_date"],
        ).drop_duplicates()
        datos_canal["channel"] = canal
        datos_por_canal.append(datos_canal)

    datos = pd.concat(datos_por_canal, ignore_index=True)
    datos["answered"] = datos["out_date"].notna()
    datos["calendar_days"] = (datos["out_date"] - datos["in_date"]).dt.days
    datos["business_days"] = np.nan

    respondidas = datos["answered"]
    inicio = (
        datos.loc[respondidas, "in_date"] + pd.Timedelta(days=1)
    ).to_numpy(dtype="datetime64[D]")
    fin = (
        datos.loc[respondidas, "out_date"] + pd.Timedelta(days=1)
    ).to_numpy(dtype="datetime64[D]")
    datos.loc[respondidas, "business_days"] = np.busday_count(inicio, fin)
    datos["on_time"] = respondidas & datos["business_days"].le(15)
    datos["pending"] = ~respondidas
    datos["year"] = datos["in_date"].dt.year

    channel_summary = (
        datos.groupby("channel", as_index=False)
        .agg(
            requests=("channel", "size"),
            answered=("answered", "sum"),
            pending=("pending", "sum"),
            median_business_days=("business_days", "median"),
            on_time_rate=("on_time", "mean"),
        )
        .sort_values("channel")
        .reset_index(drop=True)
    )
    channel_summary = channel_summary[
        [
            "channel",
            "requests",
            "answered",
            "pending",
            "median_business_days",
            "on_time_rate",
        ]
    ]

    yearly_summary = (
        datos.groupby(["year", "channel"], as_index=False)
        .agg(
            requests=("channel", "size"),
            pending=("pending", "sum"),
            on_time_rate=("on_time", "mean"),
        )
        .sort_values(["year", "channel"])
        .reset_index(drop=True)
    )

    dias = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    datos["day_name"] = pd.Categorical(datos["day_name"], categories=dias, ordered=True)
    entry_day_summary = (
        datos.groupby("day_name", observed=True, as_index=False)
        .agg(
            requests=("day_name", "size"),
            median_calendar_days=("calendar_days", "median"),
            median_business_days=("business_days", "median"),
        )
        .sort_values("day_name")
        .reset_index(drop=True)
    )
    entry_day_summary["day_name"] = entry_day_summary["day_name"].astype(str)

    directorio_salida = directorio / "submission"
    directorio_salida.mkdir(parents=True, exist_ok=True)
    channel_summary.to_csv(directorio_salida / "channel_summary.csv", index=False)
    yearly_summary.to_csv(directorio_salida / "yearly_summary.csv", index=False)
    entry_day_summary.to_csv(
        directorio_salida / "entry_day_summary.csv",
        index=False,
    )

    return channel_summary, yearly_summary, entry_day_summary

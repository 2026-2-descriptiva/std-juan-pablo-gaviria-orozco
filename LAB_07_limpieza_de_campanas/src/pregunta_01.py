import pandas as pd


def clean_campaign_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Los datos de una campaña de mercadeo bancario llegaron repartidos en diez
    archivos comprimidos, `data/bank-marketing-campaing-*.csv.gz`, con
    información mezclada del cliente, de la campaña y del contexto económico.
    Su tarea es leerlos directamente desde los archivos comprimidos, sin
    descomprimirlos a mano, y separarlos en tres tablas limpias.

    Guarde cada tabla como un CSV sin comprimir en `submission/`, sin el índice
    de Pandas y con las columnas en el orden indicado:

    1. `client.csv`: `client_id`, `age`, `job`, `marital`, `education`,
       `credit_default` y `mortgage`.
       - En `job`, elimine los puntos y cambie los guiones por guiones bajos.
       - En `education`, cambie los puntos por guiones bajos y deje el valor
         `unknown` como faltante.
       - En `credit_default` y `mortgage`, escriba 1 si el valor es `yes` y 0
         en cualquier otro caso.

    2. `campaign.csv`: `client_id`, `number_contacts`, `contact_duration`,
       `previous_campaign_contacts`, `previous_outcome`, `campaign_outcome` y
       `last_contact_date`.
       - En `previous_outcome`, escriba 1 si el valor es `success` y 0 en
         cualquier otro caso.
       - En `campaign_outcome`, escriba 1 si el valor es `yes` y 0 en
         cualquier otro caso.
       - Construya `last_contact_date` a partir de las columnas `month` y
         `day`, usando el año 2022 y el formato `AAAA-MM-DD`.

    3. `economics.csv`: `client_id`, `cons_price_idx` y
       `euribor_three_months`.

    La función también debe retornar las tres tablas, en el orden `client`,
    `campaign` y `economics`.

    Ejemplo del formato de `campaign.csv`:

        client_id,number_contacts,contact_duration,...,last_contact_date
        0,1,261,...,2022-05-13
        ...
    """

    from pathlib import Path

    directorio = Path(__file__).resolve().parents[1]
    rutas = sorted((directorio / "data").glob("bank-marketing-campaing-*.csv.gz"))
    datos = pd.concat(
        [pd.read_csv(ruta, compression="gzip", index_col=0) for ruta in rutas],
        ignore_index=True,
    )

    client = pd.DataFrame(
        {
            "client_id": datos["client_id"],
            "age": datos["age"],
            "job": datos["job"].str.replace(".", "", regex=False).str.replace(
                "-", "_", regex=False
            ),
            "marital": datos["marital"],
            "education": datos["education"]
            .str.replace(".", "_", regex=False)
            .replace("unknown", pd.NA),
            "credit_default": datos["credit_default"].eq("yes").astype(int),
            "mortgage": datos["mortgage"].eq("yes").astype(int),
        }
    ).sort_values("client_id").reset_index(drop=True)

    meses = {
        "jan": 1,
        "feb": 2,
        "mar": 3,
        "apr": 4,
        "may": 5,
        "jun": 6,
        "jul": 7,
        "aug": 8,
        "sep": 9,
        "oct": 10,
        "nov": 11,
        "dec": 12,
    }
    fechas = pd.to_datetime(
        pd.DataFrame(
            {
                "year": [2022] * len(datos),
                "month": datos["month"].map(meses),
                "day": datos["day"],
            }
        )
    )
    campaign = pd.DataFrame(
        {
            "client_id": datos["client_id"],
            "number_contacts": datos["number_contacts"],
            "contact_duration": datos["contact_duration"],
            "previous_campaign_contacts": datos["previous_campaign_contacts"],
            "previous_outcome": datos["previous_outcome"].eq("success").astype(int),
            "campaign_outcome": datos["campaign_outcome"].eq("yes").astype(int),
            "last_contact_date": fechas.dt.strftime("%Y-%m-%d"),
        }
    ).sort_values("client_id").reset_index(drop=True)

    economics = datos[
        ["client_id", "cons_price_idx", "euribor_three_months"]
    ].sort_values("client_id").reset_index(drop=True)

    directorio_salida = directorio / "submission"
    directorio_salida.mkdir(parents=True, exist_ok=True)
    client.to_csv(directorio_salida / "client.csv", index=False)
    campaign.to_csv(directorio_salida / "campaign.csv", index=False)
    economics.to_csv(directorio_salida / "economics.csv", index=False)

    return client, campaign, economics

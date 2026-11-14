import pandas as pd


def build_cohort_analysis() -> pd.DataFrame:
    """
    Una tienda quiere saber si sus clientes vuelven a comprar después de su
    primera compra. Para responder, agrupe a los clientes en cohortes según
    el mes de su primera compra y mida, mes a mes, qué proporción de cada
    cohorte vuelve a comprar. Use `data/sales.csv.gz`, que tiene una fila por
    orden con su cliente (`CustomerID`) y su fecha (`OrderDate`).

    Use estas definiciones:

    - `cohort_month`: el mes de la primera compra del cliente, escrito como
      `AAAA-MM`.
    - `period_index`: los meses transcurridos desde `cohort_month`; es 0 en el
      mes de la primera compra, 1 en el mes siguiente, y así sucesivamente.
    - `active_customers`: la cantidad de clientes distintos de la cohorte que
      compraron en ese período.
    - `cohort_size`: la cantidad de clientes de la cohorte, es decir, sus
      clientes activos en el período 0.
    - `retention_rate`: `active_customers` sobre `cohort_size`.

    Genere dos archivos en `submission/`:

    1. `cohort_retention.csv`, sin el índice de Pandas, con las columnas
       `cohort_month`, `period_index`, `active_customers`, `cohort_size` y
       `retention_rate`, y una fila por cada combinación cohorte–período
       observada, ordenadas por cohorte y período.

    2. `cohort_retention_heatmap.png`, un mapa de calor de `retention_rate`
       con una fila por cohorte (eje vertical) y una columna por período
       (eje horizontal). Muestre los valores como porcentajes. Los períodos
       que todavía no se pueden observar para una cohorte no significan
       retención cero: déjelos vacíos en el mapa.

    La función también debe retornar la tabla de retención.

    Ejemplo del formato de `cohort_retention.csv`:

        cohort_month,period_index,active_customers,cohort_size,retention_rate
        2022-01,0,100,100,1.0
        2022-01,1,26,100,0.26
        ...
    """

    from pathlib import Path

    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.ticker import PercentFormatter

    directorio = Path(__file__).resolve().parents[1]
    datos = pd.read_csv(directorio / "data" / "sales.csv.gz", compression="gzip")
    datos["OrderDate"] = pd.to_datetime(datos["OrderDate"])

    meses_orden = datos["OrderDate"].dt.to_period("M")
    meses_cohorte = (
        datos.groupby("CustomerID")["OrderDate"].transform("min").dt.to_period("M")
    )
    datos["cohort_month"] = meses_cohorte.astype(str)
    datos["period_index"] = (
        (meses_orden.dt.year - meses_cohorte.dt.year) * 12
        + meses_orden.dt.month
        - meses_cohorte.dt.month
    )

    retencion = (
        datos.groupby(["cohort_month", "period_index"])["CustomerID"]
        .nunique()
        .reset_index(name="active_customers")
    )
    tamanos_cohorte = datos.groupby("cohort_month")["CustomerID"].nunique()
    retencion["cohort_size"] = retencion["cohort_month"].map(tamanos_cohorte)
    retencion["retention_rate"] = (
        retencion["active_customers"] / retencion["cohort_size"]
    )
    retencion = retencion[
        [
            "cohort_month",
            "period_index",
            "active_customers",
            "cohort_size",
            "retention_rate",
        ]
    ].sort_values(["cohort_month", "period_index"]).reset_index(drop=True)

    matriz = retencion.pivot(
        index="cohort_month",
        columns="period_index",
        values="retention_rate",
    )
    figura, eje = plt.subplots(figsize=(12, 6))
    imagen = eje.imshow(
        np.ma.masked_invalid(matriz.to_numpy()),
        aspect="auto",
        cmap="Blues",
        vmin=0,
        vmax=1,
    )
    eje.set_xticks(range(len(matriz.columns)), matriz.columns)
    eje.set_yticks(range(len(matriz.index)), matriz.index)
    eje.set_xlabel("Período desde la primera compra (meses)")
    eje.set_ylabel("Cohorte")
    eje.set_title("Retención de clientes por cohorte")

    for fila in range(matriz.shape[0]):
        for columna in range(matriz.shape[1]):
            valor = matriz.iloc[fila, columna]
            if pd.notna(valor):
                eje.text(
                    columna,
                    fila,
                    f"{valor:.0%}",
                    ha="center",
                    va="center",
                    color="white" if valor >= 0.6 else "black",
                )

    barra = figura.colorbar(imagen, ax=eje)
    barra.ax.yaxis.set_major_formatter(PercentFormatter(1))
    figura.tight_layout()

    directorio_salida = directorio / "submission"
    directorio_salida.mkdir(parents=True, exist_ok=True)
    retencion.to_csv(directorio_salida / "cohort_retention.csv", index=False)
    figura.savefig(directorio_salida / "cohort_retention_heatmap.png")
    plt.close(figura)
    return retencion

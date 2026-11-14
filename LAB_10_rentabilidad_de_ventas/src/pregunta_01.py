import pandas as pd


def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Una cadena de suministros de oficina vende mucho, pero la gerencia
    sospecha que parte de esas ventas no deja utilidad. El archivo
    `data/superstore_orders.csv.gz` tiene una fila por línea de pedido, con
    el número de pedido (`Order ID`), las ventas (`Sales`), la utilidad
    (`Profit`), el descuento aplicado (`Discount`, como proporción), el
    segmento del cliente (`Customer Segment`) y la categoría del producto
    (`Product Category`). Una utilidad negativa significa que la línea se
    vendió con pérdida.

    Use estas definiciones:

    - Margen (`profit_margin`): utilidad sobre ventas.
    - Línea con pérdida: una línea cuya utilidad es negativa.
    - `loss_line_rate`: la proporción de líneas con pérdida.
    - `lost_profit`: la suma de las pérdidas de las líneas con pérdida,
      escrita como número positivo.
    - Rango de descuento (`discount_band`): `0%` si no hubo descuento,
      `1%-5%` si fue mayor que 0 y hasta 5 %, `6%-10%` si fue mayor que 5 % y
      hasta 10 %, y `más de 10%` en otro caso.

    Genere tres archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `profitability_summary.csv`, con una sola fila: `lines` (cantidad de
       líneas), `orders` (pedidos distintos), `sales`, `profit`,
       `profit_margin`, `loss_lines` (cantidad de líneas con pérdida),
       `loss_line_rate` y `lost_profit`.

    2. `discount_summary.csv`, con una fila por rango de descuento, en el
       orden en que se definieron arriba: `discount_band`, `lines`, `sales`,
       `profit`, `profit_margin`, `loss_line_rate` y `lost_profit`.

    3. `priority_segments.csv`, con los cinco segmentos segmento–categoría
       que más utilidad pierden: `Customer Segment`, `Product Category`,
       `lines`, `sales`, `profit`, `profit_margin` y `lost_profit`. Considere
       solamente segmentos con al menos 100 líneas y ordénelos por
       `lost_profit` de mayor a menor.

    La función también debe retornar las tres tablas, en el mismo orden.

    Ejemplo del formato de `discount_summary.csv`:

        discount_band,lines,sales,profit,profit_margin,loss_line_rate,...
        0%,166,170539.05,29472.3789,0.1728,0.488,...
        ...
    """

    from pathlib import Path

    directorio = Path(__file__).resolve().parents[1]
    datos = pd.read_csv(
        directorio / "data" / "superstore_orders.csv.gz",
        sep=";",
        decimal=",",
        compression="gzip",
    )
    perdidas = datos["Profit"] < 0
    datos["is_loss"] = perdidas
    datos["lost_profit"] = (-datos["Profit"]).where(perdidas, 0)

    profit_margin = datos["Profit"].sum() / datos["Sales"].sum()
    profitability_summary = pd.DataFrame(
        [
            {
                "lines": len(datos),
                "orders": datos["Order ID"].nunique(),
                "sales": datos["Sales"].sum(),
                "profit": datos["Profit"].sum(),
                "profit_margin": profit_margin,
                "loss_lines": int(perdidas.sum()),
                "loss_line_rate": perdidas.mean(),
                "lost_profit": datos["lost_profit"].sum(),
            }
        ]
    )

    discount_bands = ["0%", "1%-5%", "6%-10%", "más de 10%"]
    discount = datos["Discount"]
    datos["discount_band"] = "más de 10%"
    datos.loc[discount.eq(0), "discount_band"] = "0%"
    datos.loc[discount.gt(0) & discount.le(0.05), "discount_band"] = "1%-5%"
    datos.loc[discount.gt(0.05) & discount.le(0.10), "discount_band"] = "6%-10%"
    datos["discount_band"] = pd.Categorical(
        datos["discount_band"],
        categories=discount_bands,
        ordered=True,
    )

    discount_summary = (
        datos.groupby("discount_band", observed=False)
        .agg(
            lines=("Profit", "size"),
            sales=("Sales", "sum"),
            profit=("Profit", "sum"),
            loss_lines=("is_loss", "sum"),
            lost_profit=("lost_profit", "sum"),
        )
        .reset_index()
    )
    discount_summary["profit_margin"] = (
        discount_summary["profit"] / discount_summary["sales"]
    )
    discount_summary["loss_line_rate"] = (
        discount_summary["loss_lines"] / discount_summary["lines"]
    )
    discount_summary = discount_summary[
        [
            "discount_band",
            "lines",
            "sales",
            "profit",
            "profit_margin",
            "loss_line_rate",
            "lost_profit",
        ]
    ]

    priority_segments = (
        datos.groupby(["Customer Segment", "Product Category"], as_index=False)
        .agg(
            lines=("Profit", "size"),
            sales=("Sales", "sum"),
            profit=("Profit", "sum"),
            lost_profit=("lost_profit", "sum"),
        )
    )
    priority_segments = priority_segments[priority_segments["lines"] >= 100].copy()
    priority_segments["profit_margin"] = (
        priority_segments["profit"] / priority_segments["sales"]
    )
    priority_segments = priority_segments.sort_values(
        "lost_profit", ascending=False
    ).head(5)
    priority_segments = priority_segments[
        [
            "Customer Segment",
            "Product Category",
            "lines",
            "sales",
            "profit",
            "profit_margin",
            "lost_profit",
        ]
    ].reset_index(drop=True)

    directorio_salida = directorio / "submission"
    directorio_salida.mkdir(parents=True, exist_ok=True)
    profitability_summary.to_csv(
        directorio_salida / "profitability_summary.csv",
        index=False,
    )
    discount_summary.to_csv(
        directorio_salida / "discount_summary.csv",
        index=False,
    )
    priority_segments.to_csv(
        directorio_salida / "priority_segments.csv",
        index=False,
    )

    return profitability_summary, discount_summary, priority_segments

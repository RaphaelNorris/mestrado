import pandas as pd

def aggregate_demand_by_interval(df, datetime_col, h3_col, interval):
    """
    Agrega a demanda com base no índice H3 e na coluna de tempo arredondada para o intervalo especificado.

    Parâmetros:
    - df: DataFrame original.
    - datetime_col: nome da coluna de data/hora (str).
    - h3_col: nome da coluna com o índice H3 (str).
    - interval: string compatível com pandas para o intervalo de tempo ('H', '30min', '15min', etc).

    Retorna:
    - DataFrame com colunas [h3_col, rounded_time, demand]
    """
    rounded_col = f"time_{interval.replace('min', 'm').lower()}"
    df[rounded_col] = df[datetime_col].dt.floor(interval)

    ts_agg = (
        df.groupby([h3_col, rounded_col])
        .size()
        .reset_index(name="demand")
    )
    return ts_agg

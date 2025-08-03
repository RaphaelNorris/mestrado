import h3
import pandas as pd

def h3_index(df: pd.DataFrame, lat: str, lng: str, resolution: int) -> pd.DataFrame:
    df['h3'] = df.apply(
        lambda row: h3.latlng_to_cell(row[lat], row[lng], resolution),
        axis=1
    )
    return df


def fe_count_h3(df: pd.DataFrame) -> pd.DataFrame:
    df['count'] = df['h3'].map(df['h3'].value_counts())
    return df





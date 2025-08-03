import pandas as pd
from pandas import DataFrame

def features_null_nas(df: DataFrame) -> DataFrame:
    """
    Preenche valores nulos:
    - Numéricos com 0
    - Strings com 'NA'
    - Datas com 01/01/2999
    """
    df_nu = df.select_dtypes(include='number').fillna(0)
    df_str = df.select_dtypes(include='object').fillna('NA')
    df_dt = df.select_dtypes(include='datetime64[ns]').fillna(pd.Timestamp('2999-01-01'))

    df_clean = pd.concat([df_nu, df_str, df_dt], axis=1)
    df_clean = df_clean[df.columns]  # reordena colunas

    return df_clean

def features_type(df: DataFrame) -> DataFrame:
    """
    Cast das colunas para os tipos corretos
    """
    df['TX_ORIGEM_LAT'] = pd.to_numeric(df['TX_ORIGEM_LAT'])
    df['TX_ORIGEM_LNG'] = pd.to_numeric(df['TX_ORIGEM_LNG'])
    df['CD_SOLICITACAO'] = df['CD_SOLICITACAO'].astype(str)
    df['DT_REGISTRO'] = pd.to_datetime(df['DT_REGISTRO'])
    df['CD_SOLICITACAO'] = df['CD_SOLICITACAO'].astype(str)
    return df

def feature_tipo_cliente(df: DataFrame) -> DataFrame:
    """
    Cria coluna TP_CLIENTE com base em CD_EMPRESA
    """
    df['tp_cliente'] = df['CD_EMPRESA'].apply(
        lambda x: 'PJ' if pd.notnull(x) and str(x).strip() != '' else 'PF'
    )
    return df

def rename_features(df: DataFrame) -> DataFrame:
    """
    Renomeia colunas para padrão esperado e converte nomes para lowercase
    Foi renomeado de forma invertida pois no banco de dados está invertido
    """
    df.rename(columns={
        'TX_ORIGEM_LAT': 'lat',
        'TX_ORIGEM_LNG': 'lng',
        'DT_REGISTRO': 'ds',
        'CD_SOLICITACAO':'unique_id'
    }, inplace=True)

    df.columns = df.columns.str.lower()
    return df


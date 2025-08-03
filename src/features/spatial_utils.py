# Manipulação de dados
import pandas as pd

# H3 Core
import h3

# Geometria e GeoJSON
from shapely.geometry import Polygon
from geojson import Feature, FeatureCollection
import json

# Visualização com Plotly
import plotly.express as px



def docs_flow_spatial():
    """

                        +-------------------------+
                        |     DataFrame (df)      |
                        | com coluna 'h3' e       |
                        | 'unique_id'             |
                        +-------------------------+
                                    |
                                    | (entrada)
                                    v
                +-----------------------------------------+
                | generate_h3_counts_with_geometry(df)    |
                | - Agrupa por 'h3'                       |
                | - Conta IDs únicos                     |
                | - Aplica geometria com add_geometry()   |
                +-----------------------------------------+
                                    |
                                    v
                        +------------------------+
                        | DataFrame com colunas: |
                        | ['h3', 'ids', 'count', |
                        |  'geometry']           |
                        +------------------------+
                                    |
                                    |
                                    | usa
                                    v
                    +------------------------------+
                    | add_geometry(row)            |
                    | - Recebe linha com 'h3'      |
                    | - Gera Polygon invertendo    |
                    |   (lat, lng) → (lng, lat)    |
                    +------------------------------+
                                    |
                                    v
                +---------------------------------------------+
                | plot_h3_mapbox(df_gp, center_lat, center_lng)|
                | - Converte com hexagons_dataframe_to_geojson |
                | - Plota com Plotly choropleth_mapbox         |
                +---------------------------------------------+
                                    |
                                    v
                +----------------------------------+
                | hexagons_dataframe_to_geojson() |
                | - Constrói FeatureCollection     |
                | - Exporta ou retorna GeoJSON     |
                +----------------------------------+

    """

    return 

def hexagons_dataframe_to_geojson(df_hex, hex_id_field,geometry_field, value_field,file_output = None):

    list_features = []

    for i, row in df_hex.iterrows():
        feature = Feature(geometry = row[geometry_field],
                          id = row[hex_id_field],
                          properties = {"value": row[value_field]})
        list_features.append(feature)

    feat_collection = FeatureCollection(list_features)

    if file_output is not None:
        with open(file_output, "w") as f:
            json.dump(feat_collection, f)

    else :
      return feat_collection
    
def add_geometry(row):
    """
    Constrói a geometria poligonal de uma célula H3 a partir de seu índice.

    A função utiliza `h3.cell_to_boundary` para obter os vértices do hexágono H3
    correspondente ao índice presente na linha do DataFrame (`row['h3']`). 

   IMPORTANTE:
    O `cell_to_boundary` retorna uma lista de coordenadas no formato (latitude, longitude).
    No entanto, bibliotecas como `shapely` e formatos como GeoJSON esperam as coordenadas
    no padrão (longitude, latitude), ou seja, (x, y). Por isso, é necessário inverter
    a ordem dos valores antes de construir o polígono.

    Parâmetros:
    ----------
    row : pandas.Series
        Linha do DataFrame contendo ao menos uma coluna 'h3' com o índice H3.

    Retorna:
    -------
    shapely.geometry.Polygon
        Objeto poligonal representando a célula H3 no formato geométrico esperado.
    """
    boundary = h3.cell_to_boundary(row['h3'])  # retorna [(lat, lng), ...]
    return Polygon([(lng, lat) for lat, lng in boundary])  # inverter para (x, y) = (lon, lat)


def generate_h3_counts_with_geometry(df, unique_id_col='unique_id'):
    """
    Agrupa por célula H3, calcula a contagem de eventos e gera a geometria do hexágono.

    Parâmetros:
    ----------
    df : pd.DataFrame
        DataFrame com a coluna 'h3' já calculada.
    unique_id_col : str
        Nome da coluna com os identificadores dos eventos (ex: 'unique_id').

    Retorna:
    -------
    pd.DataFrame
        DataFrame com colunas: ['h3', 'ids', 'count', 'geometry']
    """
    df_gp = (
        df.groupby('h3')[unique_id_col]
        .agg(list)
        .to_frame("ids")
        .reset_index()
    )
    df_gp['count'] = df_gp['ids'].apply(len)
    df_gp['geometry'] = df_gp.apply(add_geometry, axis=1)
    return df_gp


def plot_h3_mapbox(df_gp, center_lat, center_lng, count_col='count'):
    """
    Plota mapa coroplético interativo com hexágonos H3 agregados.

    Parâmetros:
    ----------
    df_gp : pd.DataFrame
        DataFrame com colunas ['h3', 'geometry', count_col].
    center_lat : float
        Latitude central do mapa.
    center_lng : float
        Longitude central do mapa.
    count_col : str
        Nome da coluna com os valores agregados.

    Retorna:
    -------
    plotly.graph_objects.Figure
    """
    geojson_obj = hexagons_dataframe_to_geojson(
        df_gp,
        hex_id_field='h3',
        value_field=count_col,
        geometry_field='geometry'
    )

    fig = px.choropleth_mapbox(
        df_gp,
        geojson=geojson_obj,
        locations='h3',
        color=count_col,
        color_continuous_scale="Viridis",
        range_color=(0, df_gp[count_col].mean()),
        mapbox_style='carto-positron',
        zoom=10,
        center={"lat": center_lat.median(), "lon": center_lng.median()},
        opacity=0.7,
        labels={count_col: '# solicitações'}
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.show()

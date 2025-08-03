from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from src.data.processing import features_null_nas, features_type, feature_tipo_cliente, rename_features

def pipeline_data(df_raw):
    pipeline = Pipeline([
        ('cliente_tipo', FunctionTransformer(feature_tipo_cliente, validate=False)),
        ('fill_nas', FunctionTransformer(features_null_nas, validate=False)),
        ('cast_types', FunctionTransformer(features_type, validate=False)),
        ('rename_cols', FunctionTransformer(rename_features, validate=False))
    ])

    df_processado = pipeline.fit_transform(df_raw)
    return df_processado





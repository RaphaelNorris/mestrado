from cnn_sql import executar_query

# Query padrão válida
query_padrao = """
    SELECT 
        CD_SOLICITACAO, 
        TX_ORIGEM_LAT, 
        TX_ORIGEM_LNG,
        TX_DESTINO_LAT, 
        TX_DESTINO_LNG,
        TX_H3INDEX_ORIGEM, 
        DT_REGISTRO, 
        TX_STATUS
    FROM APP_SOLICITACAO_HIST 
    WHERE DT_REGISTRO >= '2020-01-01'
"""

print("Manter a query padrão? \nSim - 1 \nNão - 0")
manter_query = input().strip()

# Se o usuário escolher 0, solicita uma nova query
if manter_query == "0":
    print("Digite a query:")
    query = input()
else:
    query = query_padrao

# Nome do arquivo de saída
print("Digite o nome do arquivo (sem extensão):")
nome_arquivo = input().strip()

# Caminho seguro para salvar o arquivo
path = f"C:/Users/norris/Desktop/Mestrado/transformers/detection_anomaly/data/external/{nome_arquivo}"

# Executar a query e salvar
executar_query(query, nome_arquivo=path, salvar_em_arquivo=True)

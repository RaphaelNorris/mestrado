from dotenv import load_dotenv
import os
import pyodbc
import pandas as pd
import logging
import os

# Carregar variáveis de ambiente
load_dotenv()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def check_odbc_driver(driver_name="ODBC Driver 18 for SQL Server"):
    available = [driver for driver in pyodbc.drivers() if driver_name in driver]
    if not available:
        raise EnvironmentError(f"Driver ODBC '{driver_name}' não encontrado. Instale ou verifique o nome.")
    return available[0]

def connect_db():
    """
    Cria e retorna uma conexão com o banco de dados.
    """
    try:
        server = os.getenv('DB_SERVER')
        database = os.getenv('DB_DATABASE')
        username = os.getenv('DB_USERNAME')
        password = os.getenv('DB_PASSWORD')

        # Verificar se alguma variável está faltando
        var_map = {
            'DB_SERVER': server,
            'DB_DATABASE': database,
            'DB_USERNAME': username,
            'DB_PASSWORD': password
        }

        vars_not_in = [var for var, value in var_map.items() if not value]
        if vars_not_in:
            raise ValueError(f"As seguintes variáveis de ambiente estão faltando: {', '.join(vars_not_in)}")

        # Validar driver ODBC
        driver = check_odbc_driver()

        # Connection string
        connection_string = (
            f"DRIVER={{{driver}}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={username};"
            f"PWD={password};"
            "TrustServerCertificate=yes;"
        )

        conn = pyodbc.connect(connection_string)
        logging.info("Conexão com o banco de dados estabelecida.")
        return conn

    except Exception as e:
        logging.error(f"Erro ao conectar no banco: {e}")
        return None

def executar_query(query: str, nome_arquivo: str = None, salvar_em_arquivo: bool = True):
    """
    Executa uma query no banco de dados e salva o resultado em arquivo .parquet, se desejado.
    """
    conn = connect_db()
    if not conn:
        logging.error("Não foi possível conectar ao banco para executar a query.")
        return None

    try:
        df = pd.read_sql(query, conn)

        if salvar_em_arquivo and nome_arquivo:
            os.makedirs(os.path.dirname(nome_arquivo), exist_ok=True) if os.path.dirname(nome_arquivo) else None
            df.to_parquet(f"{nome_arquivo}.parquet", index=False)
            logging.info(f"Resultado salvo como {nome_arquivo}.parquet")

        return df

    except Exception as e:
        logging.error(f"Erro ao executar a query ou salvar o arquivo: {e}")
        return None
    finally:
        conn.close()

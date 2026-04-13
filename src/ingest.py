#1. Importação das bibliotecas necessárias
import pandas as pd     
import sqlite3
import mlflow
import os
import logging

#2. Definição de camaminhos (PATHS)

#Definindo formato de logging
LOG_DIR = "../logs"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname) -%(message)s',
    handlers=[
        logging.FileHandler("../logs/ingest.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("ingest")


RAW_DATA_PATH = "../data/raw/Telco_customer_churn.xlsx"
DB_PATH = "../data/processed/churn.db" 



#3. Função de ingestão de dados
def ingest_data():
    logger.info("Iniciando o processo de ingestão de dados.")

    try:
        #Garantir diretórios
        dir_name = os.path.dirname(DB_PATH)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
            logger.info(f"Diretório de desino criado:{dir_name}")

        if not os.path.exists(RAW_DATA_PATH):
            logger.error(f"Falha na ingestão de dados: arquivo não encontrado em {RAW_DATA_PATH}")
        
        df = pd.read_excel(RAW_DATA_PATH)
        logger.info(f"Arquivo de dados carregado com sucesso! Qtd total de linhas: {len(df)}")

        #Limpeza e Normalização de dados
        df.columns = [col.replace(" ","_").lower() for col in df.columns]
        df['total_charges'] = pd.to_numeric(df['total_charges'], errors='coerce').fillna(0)
        
        logger.info("Limpeza e padronização")

        #Carga no sqlite
        with sqlite3.connect(DB_PATH) as conn:
            df.to_sql('tb_churn_origem', conn, if_exists='replace', index=False)
            logger.info(f"Tabela 'tb_churn_origem persistida com sucesso em {DB_PATH}")

    except Exception as e:
        logger.error(f"Erro inesperado durante a ingestão {str(e)}", exc_info=True)


if __name__ == "__main__":
    os.makedirs("../logs", exist_ok=True)
    ingest_data()
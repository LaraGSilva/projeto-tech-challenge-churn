from fastapi import FastAPI, HTTPException, Path as FastAPIPath,Request
import sqlite3
import os
from pydantic import BaseModel, Field, field_validator
import time
import logging
from pathlib import Path

#Definindo formato de logging
LOG_DIR = "../logs"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname) -%(message)s',
    handlers=[
        logging.FileHandler("../logs/app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("app")


app = FastAPI(
    title="Sistema de Predição de Churn",
    description="API para consulta de predições calculadas via processo Batch diário.",
    version="1.0.0"
)

# =============================
# PATHS
# =============================
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data/processed/churn.db"


def get_db_connection():
    # Agora o caminho é calculado de forma absoluta
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    logging.info("Conexão realizada com sucesso")

    return conn
    


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "churn-prediction-api"}
    


class CustomerIDRequest(BaseModel):
    # Validamos o formato usando pattern (Regex)
    customer_id: str = Field(
        ...,
        description="ID único do cliente no formato 0000-AAAAA",
        pattern=r"^\d{4}-[A-Z]{5}$"  # 4 dígitos - 5 letras maiúsculas
    )

    # Validação customizada extra (opcional)
    @field_validator('customer_id')
    @classmethod
    def check_id_format(cls, v: str) -> str:
        if '-' not in v:
            raise ValueError('O ID deve conter um hífen')
        return v


@app.get("/prediction/{customer_id}")
def get_prediction(
    customer_id: str = FastAPIPath(..., pattern=r"^\d{4}-[A-Z]{5}$",
                            description="O ID do cliente para busca")
):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM tb_churn_predictions WHERE customerid = ?"
    result = cursor.execute(query, (customer_id,)).fetchone()
    conn.close()
    logging.info("Query executada com sucesso!")

    if result is None:
        # Se o formato estiver certo, mas o ID não existir no banco
        raise HTTPException(
            status_code=404, detail="Cliente não encontrado na base de predições.")

    return {
        "customer_id": result["customerid"],
        "churn_probability": round(result["churn_probability"], 4),
        "prediction": "Sim" if result["prediction"] == 1 else "Não"
    }

@app.get("/all-churn")
def get_all_churns():
    """Retorna todos os IDs e probabilidades de clientes com predição de Churn (1)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT customerid, churn_probability FROM tb_churn_predictions WHERE prediction = 1"
    results = cursor.execute(query).fetchall()
    conn.close()

    # Converte a lista de linhas do banco para uma lista de dicionários
    churn_list = [dict(row) for row in results]
    
    return {
        "total_churn_detected": len(churn_list),
        "clients": churn_list
    }

@app.get("/churn-info")
def get_churn_detailed_info():
    """
    Retorna informações detalhadas (origem + predição) para todos os clientes 
    com tendência de churn.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    
    query = """
        SELECT 
            p.customerid, 
            p.churn_probability, 
            o.gender,
            o.city, 
            o.payment_method, 
            o.contract, 
            o.monthly_charges
        FROM tb_churn_predictions p
        LEFT JOIN tb_churn_origem o ON p.customerid = o.customerid
        WHERE p.prediction = 1
    """
    
    try:
        results = cursor.execute(query).fetchall()
        conn.close()
        
        detailed_list = [dict(row) for row in results]
        return {
            "count": len(detailed_list),
            "data": detailed_list
        }
    except sqlite3.OperationalError as e:
        conn.close()
        logger.error(f"Erro ao acessar tabela de origem: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Erro ao cruzar dados. Verifique se a tabela de origem existe no banco."
        )
    
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    # 1. Marca o tempo de início
    start_time = time.perf_counter()
    
    # 2. Processa a requisição e obtém a resposta
    response = await call_next(request)
    
    # 3. Calcula o tempo decorrido
    process_time = time.perf_counter() - start_time
    
    # 4. Adiciona a latência nos logs do servidor
    logger.info(f"Path: {request.url.path} | Latência: {process_time:.4f}s")
    
    # 5. Opcional: Adiciona a latência no cabeçalho da resposta (útil para debug)
    response.headers["X-Process-Time"] = str(process_time)
    
    return response
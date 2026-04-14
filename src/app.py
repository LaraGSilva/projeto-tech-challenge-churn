from fastapi import FastAPI, HTTPException, Path,Request
import sqlite3
import os
from pydantic import BaseModel, Field, field_validator
import time
import logging


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

# Isso descobre onde o app.py está e monta o caminho correto para o banco
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "data", "processed", "churn.db")


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
    customer_id: str = Path(..., pattern=r"^\d{4}-[A-Z]{5}$",
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
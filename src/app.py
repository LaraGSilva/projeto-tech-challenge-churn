from fastapi import FastAPI, HTTPException, Path
import sqlite3
import pandas as pd
import os
from pydantic import BaseModel, Field, field_validator

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

    if result is None:
        # Se o formato estiver certo, mas o ID não existir no banco
        raise HTTPException(
            status_code=404, detail="Cliente não encontrado na base de predições.")

    return {
        "customer_id": result["customerid"],
        "churn_probability": round(result["churn_probability"], 4),
        "prediction": "Sim" if result["prediction"] == 1 else "Não"
    }

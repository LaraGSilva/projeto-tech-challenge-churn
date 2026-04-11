from fastapi import FastAPI, HTTPException
import sqlite3
import pandas as pd

app = FastAPI(title="Churn Query API")

def get_db_connection():
    conn = sqlite3.connect("../data/processed/churn.db")
    conn.row_factory = sqlite3.Row # Permite acessar colunas pelo nome
    return conn

@app.get("/prediction/{customer_id}")
def get_prediction(customer_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Busca a predição calculada pelo batch
    query = "SELECT * FROM tb_churn_predictions WHERE customerid = ?"
    result = cursor.execute(query, (customer_id,)).fetchone()
    conn.close()

    if result is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado na base de predições.")

    return {
        "customer_id": result["customerid"],
        "churn_probability": round(result["churn_probability"], 4),
        "prediction": "Sim" if result["prediction"] == 1 else "Não",
        "last_update": result["processed_at"]
    }
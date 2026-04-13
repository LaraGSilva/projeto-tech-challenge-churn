import sqlite3
import pandas as pd
import torch
import joblib
from preprocess import ChurnPreprocessor
from train import ChurnMLP

def run_batch_inference():
    # 1. Carregar artefatos
    processor = ChurnPreprocessor()
    processor.load_transformer("../models/preprocessor.pkl")
    
    input_size = len(processor.feature_names)
    model = ChurnMLP(input_size=input_size)
    model.load_state_dict(torch.load("../models/best_model.pt"))
    model.eval()

    # 2. Ler dados que precisam de predição
    conn = sqlite3.connect("../data/processed/churn.db")
    df_new = pd.read_sql("SELECT * FROM tb_churn_origem", conn) # Ou uma query filtrando novos IDs

    # 3. Processar e Predizer
    X_processed = processor.transform(df_new.drop(columns=['churn_value', 'customerid', 'churn_reason', 'churn_label','churn_score'], errors='ignore'))
    X_tensor = torch.tensor(X_processed, dtype=torch.float32)

    with torch.no_grad():
        outputs = model(X_tensor)
        probs = torch.sigmoid(outputs).numpy().flatten()
    
    # 4. Preparar Tabela de Resultados
    results = pd.DataFrame({
        'customerid': df_new['customerid'],
        'churn_probability': probs,
        'prediction': [1 if p > 0.5 else 0 for p in probs],
        'processed_at': pd.Timestamp.now()
    })

    # 5. Salvar no banco (Substitui a tabela a cada 24h ou faz Append)
    results.to_sql("tb_churn_predictions", conn, if_exists="replace", index=False)
    conn.close()
    print("Predição Batch concluída com sucesso!")

if __name__ == "__main__":
    run_batch_inference()
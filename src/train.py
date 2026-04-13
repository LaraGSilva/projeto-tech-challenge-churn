import os
import sqlite3
import logging
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import mlflow
import mlflow.pytorch

# Importando sua classe modular
from preprocess import ChurnPreprocessor

# 1. Configuração de Logging
LOG_DIR = "../logs"
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, "train.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("train_mlp")

# 2. Definição do Dataset PyTorch
class ChurnDataset(Dataset):
    def __init__(self, X, y):
        self.X = torch.tensor(X, dtype=torch.float32)
        self.y = torch.tensor(y.values, dtype=torch.float32).view(-1, 1)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

# 3. Arquitetura da Rede Neural (MLP)
class ChurnMLP(nn.Module):
    def __init__(self, input_size):
        super(ChurnMLP, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_size, 32),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1)
        )

    def forward(self, x):
        return self.network(x)


def run_training():
    # --- CARGA E SPLIT ---
    logger.info("Carregando dados do SQLite...")
    conn = sqlite3.connect("../data/processed/churn.db")
    df = pd.read_sql("SELECT * FROM tb_churn_origem", conn)
    conn.close()

    # Removendo colunas que causam Data Leakage (Vazamento)
    # Adicionamos churn_label e churn_score como você identificou
    cols_to_drop = ['churn_value', 'customerid', 'churn_reason', 'churn_label', 'churn_score']
    X = df.drop(columns=[c for c in cols_to_drop if c in df.columns])
    y = df['churn_value']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # --- PREPROCESSAMENTO ---
    logger.info(f"Features utilizadas: {X.columns.tolist()}")
    processor = ChurnPreprocessor()
    processor.create_pipeline(X_train)
    X_train_proc = processor.fit_transform(X_train)
    X_test_proc = processor.transform(X_test)

    os.makedirs("../models", exist_ok=True)
    processor.save_transformer("../models/preprocessor.pkl")

    # --- PREPARAÇÃO PYTORCH ---
    train_loader = DataLoader(ChurnDataset(X_train_proc, y_train), batch_size=64, shuffle=True)
    test_loader = DataLoader(ChurnDataset(X_test_proc, y_test), batch_size=64, shuffle=False)

    # --- MODELO E OTIMIZADOR ---
    model = ChurnMLP(input_size=X_train_proc.shape[1])
    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.0005) # Taxa de aprendizado ajustada

    # --- CONFIGURAÇÃO MLFLOW ---
    mlflow.set_tracking_uri("sqlite:///../mlflow.db")
    mlflow.set_experiment("Projeto_Churn_Tech_Challenge")

    with mlflow.start_run(run_name="MLP_Training_With_Metrics"):
        mlflow.log_params({
            "model_type": "MLP",
            "lr": 0.0005,
            "batch_size": 64,
            "dropout": 0.3
        })

        # --- LOOP DE TREINO COM EARLY STOPPING ---
        epochs = 100
        patience = 10
        best_loss = float('inf')
        counter = 0

        logger.info("Iniciando treinamento...")
        for epoch in range(epochs):
            model.train()
            train_losses = []
            for batch_X, batch_y in train_loader:
                optimizer.zero_grad()
                outputs = model(batch_X)
                loss = criterion(outputs, batch_y)
                loss.backward()
                optimizer.step()
                train_losses.append(loss.item())

            # Validação para Early Stopping
            model.eval()
            val_losses = []
            with torch.no_grad():
                for v_X, v_y in test_loader:
                    v_out = model(v_X)
                    v_loss = criterion(v_out, v_y)
                    val_losses.append(v_loss.item())

            avg_train_loss = np.mean(train_losses)
            avg_val_loss = np.mean(val_losses)

            # Log das perdas (LOSS) por época
            mlflow.log_metric("train_loss", avg_train_loss, step=epoch)
            mlflow.log_metric("val_loss", avg_val_loss, step=epoch)

            if (epoch + 1) % 5 == 0:
                print(f"Epoch {epoch+1}: Train Loss {avg_train_loss:.4f} | Val Loss {avg_val_loss:.4f}")

            # Lógica Early Stopping baseada na Val Loss
            if avg_val_loss < best_loss:
                best_loss = avg_val_loss
                torch.save(model.state_dict(), "../models/best_model.pt")
                counter = 0
            else:
                counter += 1
                if counter >= patience:
                    logger.info(f"Early Stopping na época {epoch+1}. Melhor Val Loss: {best_loss:.4f}")
                    break

        # --- CÁLCULO DAS MÉTRICAS DE PERFORMANCE FINAIS ---
        logger.info("Calculando métricas de performance no conjunto de teste...")
        model.load_state_dict(torch.load("../models/best_model.pt"))
        model.eval()
        
        all_preds = []
        all_labels = []
        
        with torch.no_grad():
            for v_X, v_y in test_loader:
                v_out = model(v_X)
                probs = torch.sigmoid(v_out)
                preds = (probs > 0.5).float()
                all_preds.extend(preds.numpy())
                all_labels.extend(v_y.numpy())

        # Métricas Finais
        metrics = {
            "accuracy": accuracy_score(all_labels, all_preds),
            "precision": precision_score(all_labels, all_preds, zero_division=0),
            "recall": recall_score(all_labels, all_preds, zero_division=0),
            "f1_score": f1_score(all_labels, all_preds, zero_division=0)
        }
        
        mlflow.log_metrics(metrics)
        logger.info(f"Métricas Finais: {metrics}")

        # Log do modelo no MLflow
        mlflow.pytorch.log_model(model, "model")

if __name__ == "__main__":
    run_training()
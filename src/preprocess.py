import pandas as pd
import sqlite3
import joblib
import logging
import os
from pathlib import Path
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

# =============================
# PATHS
# =============================
BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "data/processed/churn.db"
MODEL_PATH = BASE_DIR / "models/preprocessor.pkl"
LOG_DIR = BASE_DIR / "logs"

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(MODEL_PATH.parent, exist_ok=True)

# =============================
# LOGGING
# =============================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / "preprocess.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("preprocess")


# =============================
# CLASSE
# =============================
class ChurnPreprocessor:
    def __init__(self):
        self.preprocessor = None
        self.feature_names = None

    def create_pipeline(self, X):
        num_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
        cat_cols = X.select_dtypes(include=['object']).columns.tolist()

        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), num_cols),
                ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_cols)
            ]
        )

        return self.preprocessor

    def fit_transform(self, X):
        X_transformed = self.preprocessor.fit_transform(X)
        self.feature_names = self.preprocessor.get_feature_names_out()
        return X_transformed

    def transform(self, X):
        return self.preprocessor.transform(X)

    def save_transformer(self, path):
        joblib.dump(self, path)
        logger.info(f"Preprocessor salvo em {path}")

    def load_transformer(self, path):
        loaded_data = joblib.load(path)
        self.preprocessor = loaded_data.preprocessor
        self.feature_names = loaded_data.feature_names
        logger.info(f"Preprocessor carregado de {path}")


# =============================
# EXECUÇÃO
# =============================
def main():
    logger.info("Iniciando preprocessamento...")

    try:
        # Ler dados do SQLite
        with sqlite3.connect(DB_PATH) as conn:
            df = pd.read_sql("SELECT * FROM tb_churn_origem", conn)

        logger.info(f"Dados carregados: {df.shape}")

        # Separar features
        X = df.drop(columns=["churn"], errors="ignore")

        # Criar pipeline
        processor = ChurnPreprocessor()
        processor.create_pipeline(X)

        # Treinar transformer
        processor.fit_transform(X)

        # Salvar
        processor.save_transformer(MODEL_PATH)

        logger.info("Preprocessamento concluído com sucesso!")

    except Exception as e:
        logger.error(f"Erro no preprocessamento: {str(e)}", exc_info=True)


if __name__ == "__main__":
    main()
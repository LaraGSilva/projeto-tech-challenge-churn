import pandas as pd
import numpy as np
from src.preprocess import ChurnPreprocessor

def test_preprocess_transformation():
    processor = ChurnPreprocessor()
    # Criando um DataFrame de exemplo igual ao seu dataset
    df = pd.DataFrame({
        'gender': ['Male'],
        'seniorcitizen': [0],
        'tenure': [1],
        'monthlycharges': [29.85],
        'totalcharges': [29.85]
    })
    
    processor.create_pipeline(df)
    X_transformed = processor.fit_transform(df)
    
    # Verifica se o resultado não está vazio e se virou um array numérico
    assert X_transformed is not None
    assert isinstance(X_transformed, np.ndarray)
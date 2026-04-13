from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "churn-prediction-api"}

def test_prediction_invalid_id():
    # Testando a validação Pydantic/Regex que criamos
    response = client.get("/prediction/ID-INVALIDO")
    assert response.status_code == 422 # Erro de validação
from fastapi.testclient import TestClient
from src.app import app

# O TestClient simula as requisições para a API sem precisar subir o Uvicorn
client = TestClient(app)

def test_health_check():
    """Valida se o endpoint health está online"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_get_prediction_invalid_format():
    """Valida se o Pydantic bloqueia IDs com formato errado (Regex)"""
    # Formato esperado: 0000-AAAAA. Vamos enviar um errado:
    response = client.get("/prediction/abc-123")
    assert response.status_code == 422  # Unprocessable Entity
    
def test_get_prediction_not_found():
    """Valida o comportamento quando o ID é válido mas não existe no banco"""
    # Formato correto (Regex passa), mas ID inexistente (404)
    response = client.get("/prediction/0000-ZZZZZ")
    assert response.status_code == 404
    assert "detail" in response.json()

def test_process_time_header():
    """Valida se o middleware de latência está injetando o header de tempo"""
    response = client.get("/health")
    assert "X-Process-Time" in response.headers
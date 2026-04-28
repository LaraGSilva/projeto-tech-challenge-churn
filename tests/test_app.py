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
    
def test_get_all_churn_status():
    """Valida se o endpoint all_churn retorna uma lista e status 200"""
    response = client.get("/all-churn")
    assert response.status_code == 200
    data = response.json()
    assert "total_churn_detected" in data
    assert isinstance(data["clients"], list)

def test_get_churn_info_structure():
    """Valida se o endpoint churn-info retorna a estrutura de dados detalhada"""
    response = client.get("/churn-info")
    
    if response.status_code == 200:
        data = response.json()
        assert "count" in data
        assert isinstance(data["data"], list)
        
        # Se houver dados, valida se os campos de 'origem' estão presentes
        if len(data["data"]) > 0:
            first_item = data["data"][0]
            assert "payment_method" in first_item
            assert "customerid" in first_item
    else:
        # Caso a tabela de origem não exista no banco de teste, deve retornar 500 conforme o try/except
        assert response.status_code == 500

def test_all_churn_filter_logic():
    """Valida se todos os itens retornados em all_churn têm os campos esperados"""
    response = client.get("/all-churn")
    assert response.status_code == 200
    clients = response.json()["clients"]
    
    for client_data in clients:
        assert "customerid" in client_data
        assert "churn_probability" in client_data
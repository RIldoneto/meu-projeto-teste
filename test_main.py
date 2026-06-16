# test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_create_task():
    response = client.post("/tasks", json={"title": "Estudar DevOps", "description": "Terminar o trabalho"})
    assert response.status_code == 201
    assert response.json()["id"] == 1

def test_read_task():
    # Cria uma tarefa primeiro
    client.post("/tasks", json={"title": "Ler livro", "description": "Capítulo 1"})
    
    # Busca existente
    response = client.get("/tasks/2")
    assert response.status_code == 200
    
    # Busca inexistente
    response_missing = client.get("/tasks/999")
    assert response_missing.status_code == 404

def test_delete_task():
    client.post("/tasks", json={"title": "Deletar", "description": "Será deletado"})
    response = client.delete("/tasks/3")
    assert response.status_code == 204

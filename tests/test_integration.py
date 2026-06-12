from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_extraer():
    response = client.post("/api/v1/etl/extraer", json={"cantidad": 5})
    assert response.status_code == 201
    data = response.json()
    assert "registros_guardados" in data
    assert data["status"] == 201


def test_transformar():
    response = client.post("/api/v1/etl/transformar")
    assert response.status_code == 200
    data = response.json()
    assert "registros_procesados" in data
    assert data["status"] == 200


def test_reset():
    response = client.delete("/api/v1/etl/reset")
    assert response.status_code == 200
    data = response.json()
    assert "mongo_docs_eliminados" in data
    assert "mysql_rows_eliminadas" in data
    assert data["status"] == 200


def test_analitica_columna():
    response = client.get("/api/v1/analitica/columna/nombre")
    assert response.status_code in [200, 404]


def test_perfil():
    response = client.get("/api/v1/perfil/hgss4-1")
    assert response.status_code in [200, 404]
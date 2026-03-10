from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base
from app import models

# Base de datos en memoria para tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

from app.main import get_db
from app.database import Base

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


# --- Helpers ---
def crear_zona():
    response = client.post("/zonas", json={
        "nombre": "Centro",
        "codigo_postal": "28001",
        "limite_velocidad": 25
    })
    return response.json()["id"]


# --- Tests ---

def test_crear_scooter_correctamente():
    zona_id = crear_zona()
    response = client.post("/scooters", json={
        "numero_serie": "SN-001",
        "modelo": "Xiaomi",
        "bateria": 80,
        "zona_id": zona_id
    })
    assert response.status_code == 200
    data = response.json()
    assert data["numero_serie"] == "SN-001"
    assert data["zona_id"] == zona_id


def test_scooter_vinculado_a_zona():
    zona_id = crear_zona()
    response = client.post("/scooters", json={
        "numero_serie": "SN-002",
        "modelo": "Segway",
        "bateria": 60,
        "zona_id": zona_id
    })
    assert response.status_code == 200
    assert response.json()["zona_id"] == zona_id


def test_bateria_invalida_mayor_100():
    zona_id = crear_zona()
    response = client.post("/scooters", json={
        "numero_serie": "SN-003",
        "modelo": "Xiaomi",
        "bateria": 150,
        "zona_id": zona_id
    })
    assert response.status_code == 422


def test_bateria_invalida_menor_0():
    zona_id = crear_zona()
    response = client.post("/scooters", json={
        "numero_serie": "SN-004",
        "modelo": "Xiaomi",
        "bateria": -5,
        "zona_id": zona_id
    })
    assert response.status_code == 422


def test_mantenimiento_automatico():
    zona_id = crear_zona()
    # Scooter con batería baja
    client.post("/scooters", json={
        "numero_serie": "SN-010",
        "modelo": "Ninebot",
        "bateria": 10,
        "zona_id": zona_id
    })
    # Scooter con batería suficiente
    client.post("/scooters", json={
        "numero_serie": "SN-011",
        "modelo": "Ninebot",
        "bateria": 50,
        "zona_id": zona_id
    })
    response = client.post(f"/zonas/{zona_id}/mantenimiento")
    assert response.status_code == 200

    # Verificar que el de batería baja cambió de estado
    db = TestingSessionLocal()
    scooter = db.query(models.Scooter).filter(models.Scooter.numero_serie == "SN-010").first()
    assert scooter.estado == models.ScooterStatus.mantenimiento
    db.close()
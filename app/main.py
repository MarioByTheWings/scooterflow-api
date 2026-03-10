from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import models, schemas

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/zonas")
def create_zona(zona: schemas.ZoneCreate, db: Session = Depends(get_db)):
    db_zona = models.Zone(**zona.model_dump())
    db.add(db_zona)
    db.commit()
    db.refresh(db_zona)
    return db_zona


@app.post("/scooters")
def create_scooter(scooter: schemas.ScooterCreate, db: Session = Depends(get_db)):
    db_scooter = models.Scooter(**scooter.model_dump())
    db.add(db_scooter)
    db.commit()
    db.refresh(db_scooter)
    return db_scooter


@app.post("/zonas/{zona_id}/mantenimiento")
def mantenimiento(zona_id: int, db: Session = Depends(get_db)):
    """Cambia a 'mantenimiento' todos los patinetes de la zona con batería < 15%."""
    db.query(models.Scooter).filter(
        models.Scooter.zona_id == zona_id,
        models.Scooter.bateria < 15
    ).update({"estado": "mantenimiento"})
    db.commit()
    return {"mensaje": "Scooters actualizados"}
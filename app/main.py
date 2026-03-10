from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .database import SessionLocal
from . import models, schemas

app = FastAPI(title="ScooterFlow API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- ZONAS ---

@app.get("/zonas/", response_model=List[schemas.Zone])
def leer_zonas(db: Session = Depends(get_db)):
    """Leer Zonas"""
    return db.query(models.Zone).all()


@app.post("/zonas/", response_model=schemas.Zone)
def crear_zona(zona: schemas.ZoneCreate, db: Session = Depends(get_db)):
    """Crear Zona"""
    db_zona = models.Zone(**zona.model_dump())
    db.add(db_zona)
    db.commit()
    db.refresh(db_zona)
    return db_zona


@app.put("/zonas/{zona_id}", response_model=schemas.Zone)
def actualizar_zona(zona_id: int, zona: schemas.ZoneUpdate, db: Session = Depends(get_db)):
    """Actualizar Zona"""
    db_zona = db.query(models.Zone).filter(models.Zone.id == zona_id).first()
    if db_zona is None:
        raise HTTPException(status_code=404, detail="Zona no encontrada")
    
    zona_data = zona.model_dump(exclude_unset=True)
    for key, value in zona_data.items():
        setattr(db_zona, key, value)
    
    db.commit()
    db.refresh(db_zona)
    return db_zona


@app.delete("/zonas/{zona_id}")
def eliminar_zona(zona_id: int, db: Session = Depends(get_db)):
    """Eliminar Zona"""
    db_zona = db.query(models.Zone).filter(models.Zone.id == zona_id).first()
    if db_zona is None:
        raise HTTPException(status_code=404, detail="Zona no encontrada")
    
    db.delete(db_zona)
    db.commit()
    return {"mensaje": f"Zona {zona_id} eliminada"}


@app.post("/zonas/{zona_id}/mantenimiento")
def mantenimiento(zona_id: int, db: Session = Depends(get_db)):
    """Cambia a 'mantenimiento' todos los patinetes de la zona con batería < 15%."""
    db.query(models.Scooter).filter(
        models.Scooter.zona_id == zona_id,
        models.Scooter.bateria < 15
    ).update({"estado": models.ScooterStatus.mantenimiento})
    db.commit()
    return {"mensaje": "Scooters actualizados"}


# --- SCOOTERS ---

@app.post("/scooters/", response_model=schemas.Scooter)
def crear_patinete(scooter: schemas.ScooterCreate, db: Session = Depends(get_db)):
    """Crear Patinete"""
    db_scooter = models.Scooter(**scooter.model_dump())
    db_scooter.estado = models.ScooterStatus.disponible
    db.add(db_scooter)
    db.commit()
    db.refresh(db_scooter)
    return db_scooter


@app.get("/scooters/", response_model=List[schemas.Scooter])
def leer_patinetes(db: Session = Depends(get_db)):
    """Leer Patinetes"""
    return db.query(models.Scooter).all()


@app.put("/scooters/{scooter_id}", response_model=schemas.Scooter)
def actualizar_patinete(scooter_id: int, scooter: schemas.ScooterUpdate, db: Session = Depends(get_db)):
    """Actualizar Patinete"""
    db_scooter = db.query(models.Scooter).filter(models.Scooter.id == scooter_id).first()
    if db_scooter is None:
        raise HTTPException(status_code=404, detail="Patinete no encontrado")
    
    scooter_data = scooter.model_dump(exclude_unset=True)
    for key, value in scooter_data.items():
        setattr(db_scooter, key, value)
    
    db.commit()
    db.refresh(db_scooter)
    return db_scooter


@app.delete("/scooters/{scooter_id}")
def eliminar_patinete(scooter_id: int, db: Session = Depends(get_db)):
    """Eliminar Patinete"""
    db_scooter = db.query(models.Scooter).filter(models.Scooter.id == scooter_id).first()
    if db_scooter is None:
        raise HTTPException(status_code=404, detail="Patinete no encontrado")
    
    db.delete(db_scooter)
    db.commit()
    return {"mensaje": f"Patinete {scooter_id} eliminado"}
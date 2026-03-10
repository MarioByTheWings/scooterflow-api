from pydantic import BaseModel, Field
from typing import Optional


class ZoneCreate(BaseModel):
    nombre: str
    codigo_postal: str
    limite_velocidad: int


class ScooterCreate(BaseModel):
    numero_serie: str
    modelo: str
    bateria: int = Field(ge=0, le=100)
    zona_id: int
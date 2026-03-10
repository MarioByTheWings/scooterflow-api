from pydantic import BaseModel, Field
from typing import Optional


class ZoneBase(BaseModel):
    nombre: str
    codigo_postal: str
    limite_velocidad: int


class ZoneCreate(ZoneBase):
    pass


class ZoneUpdate(BaseModel):
    nombre: Optional[str] = None
    codigo_postal: Optional[str] = None
    limite_velocidad: Optional[int] = None


class Zone(ZoneBase):
    id: int

    class Config:
        from_attributes = True


class ScooterBase(BaseModel):
    numero_serie: str
    modelo: str
    bateria: int = Field(ge=0, le=100)
    zona_id: int


class ScooterCreate(ScooterBase):
    pass


class ScooterUpdate(BaseModel):
    numero_serie: Optional[str] = None
    modelo: Optional[str] = None
    bateria: Optional[int] = Field(None, ge=0, le=100)
    estado: Optional[str] = None
    puntuacion_usuario: Optional[float] = None
    zona_id: Optional[int] = None


class Scooter(ScooterBase):
    id: int
    estado: Optional[str] = None
    puntuacion_usuario: Optional[float] = None

    class Config:
        from_attributes = True
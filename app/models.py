from sqlalchemy import Column, Integer, String, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from .database import Base
import enum


class ScooterStatus(str, enum.Enum):
    disponible = "disponible"
    en_uso = "en_uso"
    mantenimiento = "mantenimiento"
    sin_bateria = "sin_bateria"


class Zone(Base):
    __tablename__ = "zones"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    codigo_postal = Column(String)
    limite_velocidad = Column(Integer)

    scooters = relationship("Scooter", back_populates="zona")


class Scooter(Base):
    __tablename__ = "scooters"

    id = Column(Integer, primary_key=True, index=True)
    numero_serie = Column(String)
    modelo = Column(String)
    bateria = Column(Integer)
    estado = Column(Enum(ScooterStatus))

    puntuacion_usuario = Column(Float, nullable=True)

    zona_id = Column(Integer, ForeignKey("zones.id"))
    zona = relationship("Zone", back_populates="scooters")
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, DATABASE_URL
from app.models import Zone, Scooter, ScooterStatus

# Use local port if running from host, otherwise use container URL
# Default DATABASE_URL is for container (db:5432)
# Here we check if we can reach 'db', otherwise we fall back to 'localhost'
# Another option is to allow user to pass it as env var.

db_url = os.getenv("DATABASE_URL", DATABASE_URL)

# Si estamos en local (fuera de Docker), 'db' no resolverá, así que probamos localhost
if "db" in db_url:
    try:
        # Intento rápido de ver si 'db' es resoluble
        import socket
        socket.gethostbyname("db")
    except socket.gaierror:
        db_url = db_url.replace("db", "localhost")

engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def populate():
    db = SessionLocal()
    try:
        # Check if tables exist, create if not (though migrations should handle this)
        # Base.metadata.create_all(bind=engine)

        print("--- Borrando datos previos (opcional) ---")
        db.query(Scooter).delete()
        db.query(Zone).delete()
        db.commit()

        print("--- Insertando Zonas ---")
        z1 = Zone(nombre="Centro Histórico", codigo_postal="29001", limite_velocidad=20)
        z2 = Zone(nombre="Teatinos", codigo_postal="29010", limite_velocidad=25)
        z3 = Zone(nombre="Malagueta", codigo_postal="29016", limite_velocidad=15)
        db.add_all([z1, z2, z3])
        db.commit()
        db.refresh(z1)
        db.refresh(z2)
        db.refresh(z3)

        print("--- Insertando Patinetes ---")
        s1 = Scooter(numero_serie="SF-001", modelo="Xiaomi M365", bateria=85, estado=ScooterStatus.disponible, zona_id=z1.id, puntuacion_usuario=4.5)
        s2 = Scooter(numero_serie="SF-002", modelo="Ninebot G30", bateria=40, estado=ScooterStatus.disponible, zona_id=z1.id, puntuacion_usuario=4.8)
        s3 = Scooter(numero_serie="SF-003", modelo="Xiaomi Pro 2", bateria=10, estado=ScooterStatus.sin_bateria, zona_id=z2.id, puntuacion_usuario=3.9)
        s4 = Scooter(numero_serie="SF-004", modelo="Segway P100", bateria=95, estado=ScooterStatus.mantenimiento, zona_id=z3.id)
        
        db.add_all([s1, s2, s3, s4])
        db.commit()

        print("\n" + "="*50)
        print("POBLADO DE DATOS FINALIZADO EXITOSAMENTE")
        print("="*50 + "\n")

        print("--- DATOS EN LA BASE DE DATOS ---\n")
        
        print(f"{'ID':<4} | {'ZONA':<20} | {'C.P.':<7} | {'VEL. MÁX':<8}")
        print("-" * 50)
        zones = db.query(Zone).all()
        for z in zones:
            print(f"{z.id:<4} | {z.nombre:<20} | {z.codigo_postal:<7} | {z.limite_velocidad:<8}")

        print("\n" + f"{'ID':<4} | {'S/N':<8} | {'MODELO':<15} | {'BAT %':<6} | {'ESTADO':<15} | {'ZONA':<15} | {'SCORE'}")
        print("-" * 80)
        scooters = db.query(Scooter).all()
        for s in scooters:
            zona_nombre = s.zona.nombre if s.zona else "N/A"
            score = s.puntuacion_usuario if s.puntuacion_usuario is not None else "-"
            print(f"{s.id:<4} | {s.numero_serie:<8} | {s.modelo:<15} | {s.bateria:<6} | {s.estado.value:<15} | {zona_nombre:<15} | {score}")

    except Exception as e:
        db.rollback()
        print(f"Error durante el poblado: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    populate()

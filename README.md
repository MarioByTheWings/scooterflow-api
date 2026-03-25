# ScooterFlow API

API de gestión de flota de patinetes eléctricos.

## Requisitos
- Docker y Docker Compose instalados.

## Levantar el proyecto

```bash
docker compose up --build
```

## Ejecutar migraciones Alembic y poblar la base de datos

```bash
docker compose exec api alembic upgrade head && docker compose exec api python populate_db.py
```

La API estará disponible en: http://localhost:8000/docs

## Ejecutar tests

```bash
pytest
```
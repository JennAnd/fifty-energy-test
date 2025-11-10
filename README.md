# Sensor Readings App

A fullstack application for managing sensors and their readings.

- **Backend:** Django 5 + Django Ninja (TokenAuth, PostgreSQL)
- **Frontend:** Vanilla HTML, CSS, JavaScript
- **Database:** PostgreSQL (Dockerized)
- **Testing:** `pytest`
- **Seed data:** `sensor_readings_wide.csv`

---

## Project structure

```
backend/        # Django configuration (settings, urls, etc.)
core/        # Main Django app (models, API, management commands)
frontend/       # Static HTML, CSS, and JS
sensor_readings_wide.csv
docker-compose.yml
Makefile
README.md
```

---

## Setup

### 1. Environment

Create a `.env` file in the root directory:

```bash
DJANGO_SECRET_KEY="change-me"
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

POSTGRES_DB=sensordb
POSTGRES_USER=sensoruser
POSTGRES_PASSWORD=sensorpass
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

---

### 2. Run locally

```bash
docker compose down -v      # optional cleanup
make up      # build and start containers
make migrate      # apply migrations
make seed      # load demo data from CSV
```

---

### 3. Start the frontend

```bash
cd frontend
python -m http.server 5500
```

Then open:  
[http://127.0.0.1:5500/index.html](http://127.0.0.1:5500/index.html)

From the start page, you can **register a new account** or **log in**.  
After logging in, you can navigate to **Sensors** and view each sensor’s details.

---

## API overview

### Authentication

```bash
POST /api/auth/register
POST /api/auth/login
```

Both endpoints return a token used for all protected requests:

```
Authorization: Bearer <token>
```

---

### Sensors

```bash
GET    /api/sensors
POST   /api/sensors
GET    /api/sensors/{id}
PUT    /api/sensors/{id}
DELETE /api/sensors/{id}
```

**Query parameters:**

- `q` → search by name or type
- `page` → specify which page to load (starts from 1)

---

### Readings

```bash
GET  /api/sensors/{sensor_id}/readings
POST /api/sensors/{sensor_id}/readings
```

**Query parameters:**

- `timestamp_from`
- `timestamp_to`
- `page`

---

## Run tests

```bash
make test
# or:
docker compose exec web pytest -q
```

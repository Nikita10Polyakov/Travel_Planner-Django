# Travel Planner

This repository contains a small Django REST API for managing travel projects and places.

**Quick links**
- Swagger UI (runtime): http://localhost:8000/swagger/
- Redoc (runtime): http://localhost:8000/redoc/
- OpenAPI spec (checked-in): docs/openapi.yaml

**Requirements**
- Python 3.10+ (recommended)

Setup
-----

1. Create and activate a virtual environment

```bash
python -m venv venv
# Windows (cmd):
venv\Scripts\activate
# PowerShell:
.\venv\Scripts\Activate.ps1
```

2. Install dependencies

```bash
pip install django djangorestframework drf-yasg drf-nested-routers requests
```

3. Apply migrations and create superuser (optional for admin)

```bash
python travel_planner/manage.py migrate
python travel_planner/manage.py createsuperuser
```

Run (development)
-----------------

Start the dev server:

```bash
python travel_planner/manage.py runserver
```

By default the API is mounted under `/api/`.


API overview
------------
The main resources are `projects` and nested `places`. Endpoints (base path `/api/`):

- `GET /api/projects/` — list projects
- `POST /api/projects/` — create project (optionally with `places` array)
- `GET /api/projects/{id}/` — retrieve project
- `PUT/PATCH /api/projects/{id}/` — update project
- `DELETE /api/projects/{id}/` — delete project (fails if project has visited places)

- `GET /api/projects/{project_id}/places/` — list places for a project
- `POST /api/projects/{project_id}/places/` — create place (body requires `external_id`)
- `GET /api/projects/{project_id}/places/{id}/` — retrieve place
- `PUT/PATCH /api/projects/{project_id}/places/{id}/` — update place (setting `visited` may mark project completed)
- `DELETE /api/projects/{project_id}/places/{id}/` — delete place

Example requests
----------------

Create a project with one place (example uses Art Institute external_id `129884`):

```bash
curl -X POST http://localhost:8000/api/projects/ \
	-H "Content-Type: application/json" \
	-d '{"name":"My Trip","description":"Test","start_date":"2026-02-18","places":[{"external_id":"129884"}]}'
```

Add a place to an existing project (project id = 1):

```bash
curl -X POST http://localhost:8000/api/projects/1/places/ \
	-H "Content-Type: application/json" \
	-d '{"external_id":"129884","notes":"Must see"}'
```

Mark a place visited (toggle `visited`):

```bash
curl -X PATCH http://localhost:8000/api/projects/1/places/5/ \
	-H "Content-Type: application/json" \
	-d '{"visited":true}'
```

API docs and Postman
--------------------
- Runtime Swagger UI is available at `/swagger/` (runs off `drf_yasg`) when the dev server is running.
- A checked-in OpenAPI 3.0 spec is at `docs/openapi.yaml` - you can import it into Postman or other tools.

Notes
-----
- The `projects` create serializer accepts an optional `places` array to create places along with the project. Each place must include `external_id`; the server will validate it against the Art Institute API.
- Maximum 10 places per project; duplicate `external_id` within the same project are rejected.

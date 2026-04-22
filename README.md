# BI Platform (Single Folder, FastAPI + Jinja + PostgreSQL)

This revision consolidates backend and frontend into one deployable app folder (`bi_app/`) with **FastAPI APIs + Jinja frontend templates**.

## Folder structure

```text
.
├── bi_app/
│   ├── app/
│   │   ├── core/                # settings + security helpers
│   │   ├── db/                  # engine/session/base
│   │   ├── routers/             # auth, data, analysis, pages
│   │   ├── services/            # file extraction, pattern engine, AI layer
│   │   ├── static/              # CSS/JS assets for Jinja frontend
│   │   ├── templates/           # Jinja UI pages
│   │   ├── deps.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── main.py
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml
└── README.md
```

## Why this change
- Use **Jinja** as requested for the frontend layer.
- Keep frontend + backend in a **single folder** for simpler deployment and ownership.
- Keep API contracts required by the original BI workflow.

## Run with Docker

```bash
docker-compose up --build
```

- App: http://localhost:8000
- Health: http://localhost:8000/health
- API docs: http://localhost:8000/docs

## Core API endpoints

### Auth
- `POST /api/v1/auth/signup`
- `POST /api/v1/auth/login`
- `GET /api/v1/me`

### Data
- `POST /api/v1/upload`
- `GET /api/v1/uploads`
- `GET /api/v1/company/{id}`
- `GET /api/v1/summary/{id}`

### Analysis
- `POST /api/v1/analyze`
- `GET /api/v1/relationship/{id}`

## Business flow
1. Sign up / Login from Jinja page (`/`)
2. Upload Company A and Target Company (`/app`)
3. Parsing + extraction + metadata storage
4. Pattern signature check
   - Known: rule normalization
   - Unknown/conflict: AI normalization + persist new pattern/rule
5. Save normalized companies + summaries
6. Run relationship analysis
7. View output in dashboard panel / history endpoint

## Notes
- AI service is pluggable; mock mode is used without provider key.
- Upload supports DOC/DOCX/PDF/Excel/JSON/TXT + copy-paste text.
- Max upload size is 25MB.

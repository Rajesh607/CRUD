# Business Intelligence Platform (Full Stack)

Production-style BI web application with secure auth, ingestion, pattern-driven normalization, AI abstraction, and relationship analysis.

## 1) Project Structure

```text
.
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── deps.py
│   │   │   ├── router.py
│   │   │   └── routes/
│   │   │       ├── auth.py
│   │   │       ├── data.py
│   │   │       └── analysis.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── security.py
│   │   ├── db/
│   │   │   ├── base.py
│   │   │   ├── init_db.py
│   │   │   └── session.py
│   │   ├── engines/pattern_engine.py
│   │   ├── models/models.py
│   │   ├── schemas/
│   │   │   ├── auth.py
│   │   │   └── company.py
│   │   ├── services/ai_service.py
│   │   ├── utils/file_parser.py
│   │   └── main.py
│   ├── alembic/
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/client.ts
│   │   ├── components/
│   │   ├── contexts/AuthContext.tsx
│   │   ├── pages/
│   │   ├── types/index.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
└── README.md
```

## 2) Architecture Overview

### Backend (FastAPI + SQLAlchemy + PostgreSQL)
- **Auth module**: JWT signup/login/me endpoints with bcrypt hashing.
- **Data ingestion module**: supports DOC/DOCX/PDF/Excel/JSON/text input; validates size and format.
- **Parsing/extraction**: detects file types and extracts text/metadata.
- **Pattern engine**:
  - Generates signature from content.
  - If known signature exists, applies rule-based normalization.
  - If unknown, calls AI service normalization and stores new pattern/rule.
- **AI service layer**:
  - `normalize_unknown_pattern()`
  - `summarize_company()`
  - `analyze_relationship()`
  - Runs in mock mode if API key absent.
- **Relationship engine**: score-based insights + natural-language summary.

### Frontend (React + TypeScript + Vite + Tailwind)
- Auth pages (signup/login).
- Protected dashboard + upload flows for Company A and Target.
- Summary, relationship analysis, combined results, and history pages.
- Axios client with JWT interceptor.

## 3) Setup Instructions

### Docker (recommended)
```bash
docker-compose up --build
```

Services:
- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`
- Swagger docs: `http://localhost:8000/docs`
- PostgreSQL: `localhost:5432`

### Local backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Local frontend
```bash
cd frontend
npm install
npm run dev
```

## 4) API Endpoints

### Auth
- `POST /api/v1/auth/signup`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`

### Data
- `POST /api/v1/upload`
- `GET /api/v1/uploads`
- `GET /api/v1/company/{id}`
- `GET /api/v1/summary/{id}`

### Analysis
- `POST /api/v1/analyze`
- `GET /api/v1/relationship/{id}`

## 5) Sample API Calls

### Signup
```bash
curl -X POST http://localhost:8000/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"analyst@demo.com","password":"secret123","role":"analyst"}'
```

### Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"analyst@demo.com","password":"secret123"}'
```

### Upload Company A (copy-paste)
```bash
curl -X POST http://localhost:8000/api/v1/upload \
  -H "Authorization: Bearer <TOKEN>" \
  -F "company_type=company_a" \
  -F "input_text=Company Name: Acme Corp\nIndustry: SaaS\nCountry: US"
```

### Analyze relationship
```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"company_a_id":1,"target_company_id":2}'
```

## 6) Security + Non-Functional Coverage
- JWT protected routes for upload/data/analysis.
- Password hashing with bcrypt.
- File size/type validation.
- Input schema validation via Pydantic.
- Modular clean architecture.
- Mockable AI abstraction for portability.

## 7) Basic Tests
Run backend tests:
```bash
cd backend && pytest
```

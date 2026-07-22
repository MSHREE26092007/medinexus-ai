# MediNexus AI — Autonomous Offline Clinical Intelligence Platform

Hackathon build. Phase 1: core foundation, patient CRUD, clinical dashboard.

## Quick Start

**Backend** (Python 3.11+):
```bash
cd backend
pip install -r requirements.txt
python -m app.seed          # seed 30 demo patients (once)
uvicorn app.main:app --reload --port 8000
```
API docs: http://127.0.0.1:8000/docs

**Frontend** (Node 18+):
```bash
cd frontend
npm install
npm run dev
```
Open http://localhost:5173 — `/api` requests proxy to FastAPI automatically.

## Structure
```
backend/app/
  database.py      # engine + session (SQLite, swap URL for Postgres)
  models.py        # Patient, VitalsHistory, MedicalReport, Consultation
  schemas.py       # Pydantic request/response models
  seed.py          # demo data generator
  routers/
    patients.py    # CRUD + vitals endpoints
    dashboard.py   # analytics stats
frontend/src/
  api.js           # axios client
  App.jsx          # shell (sidebar + main)
  components/      # Sidebar, StatCard, PatientTable
  pages/Dashboard.jsx
```

## Roadmap
- [x] Phase 1 (h 1–8): DB schema, Patient CRUD, dashboard UI
- [ ] Phase 2: RAG knowledge base (FAISS + Ollama + LangChain)
- [ ] Phase 3: Live vitals streaming (WebSockets + sensor sim + Plotly)
- [ ] Phase 4: ML risk prediction
- [ ] Phase 5: Report generation (ReportLab / python-docx) + AI Orchestrator

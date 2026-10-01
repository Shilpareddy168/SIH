# AIMinds – SIH 2026 (PS 26101) learning prototype
Stack from the PPT: React (Vite) · Python + FastAPI · LLM + NLP + RAG (ChromaDB) · PostgreSQL · REST APIs

## Run the backend
    cd backend
    python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
    pip install -r requirements.txt
    export ANTHROPIC_API_KEY=your_key                      # needed for quiz generation
    # optional: export DATABASE_URL=postgresql://user:pass@localhost:5432/aiminds
    uvicorn main:app --reload                              # docs at http://localhost:8000/docs

## Run the frontend
    cd frontend && npm install && npm run dev              # http://localhost:5173

## Learn by building (suggested order)
1. competencies.py + /api/assessment: open /docs and call the endpoints by hand.
2. db.py: switch SQLite to PostgreSQL, inspect the `results` table.
3. App.jsx: follow one click from React state to fetch to FastAPI to DB.
4. rag.py: upload a PDF, print the chunks, see what retrieve() returns.
5. quiz.py: change the prompt, then see how validation protects the API.
## Exercises
- Grade quiz answers on the server. Add login + role-based access. Replace sample iGOT data.
- Add pgvector instead of ChromaDB. Add a human-review queue for generated questions. Write pytest tests for analyse().

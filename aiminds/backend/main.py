from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import igot, quiz, rag
from competencies import COMPETENCIES, analyse
from db import Result, Session

app = FastAPI(title="AIMinds Learning Platform")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], allow_methods=["*"], allow_headers=["*"])

def save_result(user, kind, score, total):
    with Session() as s:
        s.add(Result(user=user, kind=kind, score=score, total=total)); s.commit()

@app.get("/api/assessment")
def get_assessment():
    """Questions WITHOUT answers."""
    return [{"id": cid, "name": c["name"], "questions": [{"q": q["q"], "options": q["options"]} for q in c["questions"]]}
            for cid, c in COMPETENCIES.items()]

class Submit(BaseModel):
    user: str
    answers: dict[str, list[int]]

@app.post("/api/assessment/submit")
def submit(body: Submit):
    report = analyse(body.answers)
    save_result(body.user, "assessment", sum(r["correct"] for r in report), sum(r["total"] for r in report))
    gaps = sorted((r for r in report if r["level"] != "strong"), key=lambda r: r["correct"])  # biggest gap first
    path = [{"competency": r["name"], "courses": igot.courses_for(r["id"])[: 2 if r["level"] == "gap" else 1]} for r in gaps]
    return {"report": report, "learning_path": path}

@app.post("/api/materials")
async def upload(user: str = Form(...), file: UploadFile = File(...)):
    text = rag.extract_text(await file.read(), file.filename)
    if not text.strip():
        raise HTTPException(400, "No text could be extracted from this file")
    return {"chunks_indexed": rag.index(user, file.filename, text)}

class QuizReq(BaseModel):
    user: str
    n: int = 5

@app.post("/api/quiz")
def generate(body: QuizReq):
    chunks = rag.retrieve(body.user, "key concepts, definitions and methods")
    if not chunks:
        raise HTTPException(400, "Upload learning material first")
    mcqs = quiz.make_mcqs("\n---\n".join(chunks), body.n)
    if not mcqs:
        raise HTTPException(502, "The model returned no valid questions. Try again.")
    return mcqs   # TODO (exercise): store answers server-side and grade there

class QuizScore(BaseModel):
    user: str
    score: int
    total: int

@app.post("/api/quiz/score")
def quiz_score(body: QuizScore):
    save_result(body.user, "quiz", body.score, body.total); return {"ok": True}

@app.get("/api/progress/{user}")
def progress(user: str):
    with Session() as s:
        rows = s.query(Result).filter_by(user=user).order_by(Result.created.desc()).all()
    return [{"kind": r.kind, "score": r.score, "total": r.total, "date": str(r.created)[:10]} for r in rows]

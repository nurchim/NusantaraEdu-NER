from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from app.inference import get_nlp, predict, quiz_questions
from app.schemas import PredictRequest, PredictResponse, QuizResponse

ROOT = Path(__file__).resolve().parents[1]
WEB_INDEX = ROOT / "web" / "index.html"
MODEL_MANIFEST = ROOT / "models" / "production" / "manifest.json"

app = FastAPI(
    title="NusantaraEdu-NER",
    version="1.0.0",
    description="AI untuk mengenali entitas budaya Indonesia dari teks Bahasa Indonesia.",
    docs_url="/api/docs",
    redoc_url=None,
)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def home():
    if not WEB_INDEX.exists():
        raise HTTPException(status_code=500, detail="Interface web tidak ditemukan.")
    return HTMLResponse(WEB_INDEX.read_text(encoding="utf-8"))


@app.get("/api", response_class=HTMLResponse, include_in_schema=False)
def api_home():
    return home()


@app.get("/api/health")
def health():
    try:
        nlp = get_nlp()
        labels = sorted(nlp.get_pipe("ner").labels) if "ner" in nlp.pipe_names else []
        return {
            "status": "ok",
            "model": nlp.meta.get("name", "nusantara_ner"),
            "pipeline": list(nlp.pipe_names),
            "label_count": len(labels),
        }
    except Exception as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.get("/api/model-info")
def model_info():
    if not MODEL_MANIFEST.exists():
        return {"status": "missing", "model_path": "models/production/model-best"}
    return {
        "status": "ok",
        **json.loads(MODEL_MANIFEST.read_text(encoding="utf-8")),
    }


@app.post("/api/predict", response_model=PredictResponse)
def api_predict(payload: PredictRequest):
    try:
        entities = predict(payload.text)
        return {"text": payload.text, "entities": entities, "model_loaded": True}
    except Exception as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.post("/api/quiz", response_model=QuizResponse)
def api_quiz(payload: PredictRequest):
    try:
        return {"text": payload.text, "questions": quiz_questions(payload.text)}
    except Exception as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

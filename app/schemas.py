from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class PredictRequest(BaseModel):
    text: str = Field(min_length=2, max_length=5000)

    @field_validator("text")
    @classmethod
    def normalize_text(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 2:
            raise ValueError("Teks terlalu pendek.")
        return value


class EntityOut(BaseModel):
    text: str
    label: str
    start: int
    end: int


class PredictResponse(BaseModel):
    text: str
    entities: list[EntityOut]
    model_loaded: bool


class QuizQuestion(BaseModel):
    prompt: str
    answer: str
    label: str


class QuizResponse(BaseModel):
    text: str
    questions: list[QuizQuestion]

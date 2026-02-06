from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

from src.agents import answer_question_text

app = FastAPI(title="Samsung Phone Advisor", version="0.1.0")


class AskBody(BaseModel):
    question: str


@app.get("/")
def home():
    return {"ok": True, "msg": "Samsung Phone Advisor API is running"}


@app.post("/ask", response_class=PlainTextResponse)
def ask(body: AskBody):
    return answer_question_text(body.question)

from fastapi import FastAPI
from pydantic import BaseModel
from rag_engine import ask_question

app = FastAPI()

class Question(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "Weed API is running"}

@app.post("/ask")
def ask(data: Question):
    answer = ask_question(data.question, [])
    return {"answer": answer}
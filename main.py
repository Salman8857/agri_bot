from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from rag_engine import ask_question

app = FastAPI()

class Question(BaseModel):
    question: str

app.add_middleware(
    CORSMiddleware,allow_origins=["https://your-frontend-name.onrender.com"]
)

@app.get("/")
def home():
    return {"message": "Weed API is running"}

@app.post("/ask")
def ask(data: Question):
    answer = ask_question(data.question, [])
    return {"answer": answer}
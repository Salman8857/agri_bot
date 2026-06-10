from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from rag_engine import ask_question
import gradio as gr

app = FastAPI()

class Question(BaseModel):
    question: str

app.add_middleware(
    CORSMiddleware,allow_origins=[]
)

@app.get("/")
def home():
    return {"message": "Weed API is running"}

@app.post("/ask")
def ask(data: Question):
    answer = ask_question(data.question, [])
    return {"answer": answer}



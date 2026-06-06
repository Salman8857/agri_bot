
import gradio as gr
from rag_engine import ask_question

def respond(message, history):
    rag_history = []

    if history:
        for item in history:
            if isinstance(item, dict):
                rag_history.append(item)

    answer = ask_question(message, rag_history)
    return answer

demo = gr.ChatInterface(
    fn=respond,
    title="Weed Management Assistant",
    description="Ask questions about weeds from the PDF guide.",
    examples=[
        "How to control Canada thistle?",
        "What are the keys to ID for musk thistle?",
        "What is the lifecycle of bull thistle?",
        "Herbicide timing for salt cedar?",
    ],
)

demo.launch()
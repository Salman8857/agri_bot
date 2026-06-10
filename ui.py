
# import gradio as gr
# from rag_engine import ask_question

# def respond(message, history):
#     rag_history = []

#     if history:
#         for item in history:
#             if isinstance(item, dict):
#                 rag_history.append(item)

#     answer = ask_question(message, rag_history)
#     return answer

# demo = gr.ChatInterface(
#     fn=respond,
#     title="Weed Management Assistant",
#     description="Ask questions about weeds from the PDF guide.",
#     examples=[
#         "How to control Canada thistle?",
#         "What are the keys to ID for musk thistle?",
#         "What is the lifecycle of bull thistle?",
#         "Herbicide timing for salt cedar?",
#     ],
# )

# demo.launch()



import gradio as gr
from rag_engine import ask_question

CSS = """
footer {display:none}

.gradio-container{
    max-width: 100% !important;
    margin: 0 !important;
}

#chatbot{
    height: 75vh;
}

h1{
    text-align:center;
}
"""

def respond(message, history):
    answer = ask_question(message, history)

    history.append(
        {"role": "user", "content": message}
    )

    history.append(
        {"role": "assistant", "content": answer}
    )

    return "", history

with gr.Blocks(theme=gr.themes.Soft()) as demo:

    gr.Markdown(
        """
        # 🌿 Weed Management Assistant
        Ask questions from the weed management guide.
        """
    )

    chatbot = gr.Chatbot(
        elem_id="chatbot",
        type="messages"
    )

    with gr.Row():
        msg = gr.Textbox(
            placeholder="Ask about weeds...",
            scale=9,
            container=False
        )

        send = gr.Button(
            "Send",
            scale=1
        )

    msg.submit(
        respond,
        [msg, chatbot],
        [msg, chatbot]
    )

    send.click(
        respond,
        [msg, chatbot],
        [msg, chatbot]
    )

demo.launch(css=CSS)
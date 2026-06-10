import gradio as gr
from rag_engine import ask_question

CSS = """
html, body {
    height: 100%;
    margin: 0;
    overflow-y: auto !important;
}

.gradio-container {
    max-width: 100% !important;
    margin: 0 !important;
    min-height: 100vh !important;
    padding: 0 !important;
    background: #f9fafb !important;
}

#header {
    display: flex !important;
    align-items: center !important;
    padding: 16px 24px !important;
    background: linear-gradient(135deg, #166534, #15803d) !important;
    flex-shrink: 0 !important;
}
#clear-btn {
    background: rgba(255,255,255,0.15) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
    border-radius: 8px !important;
    font-size: 13px !important;
    padding: 6px 16px !important;
    cursor: pointer !important;
}
#clear-btn:hover {
    background: rgba(255,255,255,0.25) !important;
}

#chatbot {
    height: 70vh !important;
    overflow-y: auto !important;
    border: none !important;
    background: transparent !important;
    padding: 16px 24px !important;
}

#examples {
    padding: 8px 24px !important;
    display: flex !important;
    gap: 8px !important;
    flex-wrap: wrap !important;
    background: white !important;
    border-top: 1px solid #e5e7eb !important;
    border-bottom: 1px solid #e5e7eb !important;
    flex-shrink: 0 !important;
}
#examples button {
    font-size: 12px !important;
    border-radius: 20px !important;
    background: #f0fdf4 !important;
    border: 1px solid #bbf7d0 !important;
    color: #166534 !important;
    padding: 4px 16px !important;
    font-weight: 500 !important;
}
#examples button:hover {
    background: #dcfce7 !important;
    border-color: #86efac !important;
}
#input-row {
    padding: 12px 24px !important;
    border-top: 1px solid #e5e7eb !important;
    background: white !important;
    flex-shrink: 0 !important;
    gap: 8px !important;
}
#send-btn {
    background: #15803d !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 10px 24px !important;
    cursor: pointer !important;
}
#send-btn:hover {
    background: #166534 !important;
}
footer {
    display: none !important;
}
"""

EXAMPLES = [
    "How to control Canada thistle?",
    "Keys to ID musk thistle",
    "Bull thistle lifecycle",
    "Herbicide timing for salt cedar",
]

def respond(message, history):
    if not message or not message.strip():
        return "", history

    rag_history = []

    for user_msg, bot_msg in history:
        rag_history.append({"role": "user", "content": user_msg})
        rag_history.append({"role": "assistant", "content": bot_msg})

    answer = ask_question(message, rag_history)

    history.append((message, answer))

    return "", history


def handle_submit(message, history):
    if not message or not message.strip():
        return "", history

    if history is None:
        history = []

    rag_history = history.copy()

    answer = ask_question(message, rag_history)

    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": answer})

    return "", history

def clear_chat():
    return "", []

with gr.Blocks(title="Weed Management Assistant") as demo:
    with gr.Row(elem_id="header"):
        with gr.Column(scale=9, min_width=0):
            gr.HTML(
                '<div style="color:white">'
                '<h2 style="margin:0;font-size:22px;font-weight:600">🌿 Weed Management Assistant</h2>'
                '<p style="margin:4px 0 0 0;font-size:13px;opacity:0.9">Ask questions from the weed management guide.</p>'
                "</div>"
            )
        with gr.Column(scale=1, min_width=80):
            clear_btn = gr.Button("🗑️ Clear", elem_id="clear-btn", size="sm")

    chatbot = gr.Chatbot(
    elem_id="chatbot",
    height=650,
    show_label=False,
    # type="messages"
)

    example_btns = []
    example_states = []
    with gr.Row(elem_id="examples"):
        for ex in EXAMPLES:
            btn = gr.Button(ex, size="sm")
            state = gr.State(ex)
            example_btns.append(btn)
            example_states.append(state)

    with gr.Row(elem_id="input-row"):
        msg = gr.Textbox(
            placeholder="Ask about weeds...",
            scale=9,
            container=False,
        )
        send = gr.Button("Send", scale=1, elem_id="send-btn", variant="primary")

    msg.submit(handle_submit, [msg, chatbot], [msg, chatbot])
    send.click(handle_submit, [msg, chatbot], [msg, chatbot])
    clear_btn.click(clear_chat, None, [msg, chatbot])

    for btn, state in zip(example_btns, example_states):
        btn.click(handle_submit, [state, chatbot], [msg, chatbot])

demo.launch(
    theme=gr.themes.Soft(),
    css=CSS
)

import os
import requests
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate

load_dotenv()

PDF_PATH = "docs/weeds.pdf"
PERSIST_DIR = ".chroma_db"
PDF_URL = "https://sam.extension.colostate.edu/wp-content/uploads/sites/2/2019/06/NoxWeedMangementGuide2019LasAnimas.pdf"

os.makedirs("docs", exist_ok=True)

if not os.path.exists(PDF_PATH):
    response = requests.get(PDF_URL)
    response.raise_for_status()

    with open(PDF_PATH, "wb") as f:
        f.write(response.content)

embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

vector_store = Chroma(
    collection_name="weed_management_system",
    embedding_function=embedding_model,
    persist_directory=PERSIST_DIR,
)

if vector_store._collection.count() == 0:
    loader = PyPDFLoader(PDF_PATH)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(docs)
    vector_store.add_documents(chunks)

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

answer_prompt = PromptTemplate.from_template("""
You are a Weed Management Assistant.

Rules:
- Answer ONLY from the PDF context.
- Do NOT use outside knowledge.
- Do NOT guess.
- If the answer is not in the PDF context, say:
  "I could not find enough information in the PDF."
- If the user asks a follow-up question, use the chat history to understand it.
- Keep answers simple and farmer-friendly.

Chat History:
{chat_history}

Question:
{question}

PDF Context:
{context}

Return this format:


Answer:
-

Suggested follow-up questions:
-

""")

reformulation_prompt = PromptTemplate.from_template("""
Rewrite the current question into a complete standalone question.

Use chat history if the user asks a follow-up like:
"identification", "control", "herbicide", "timing", "lifecycle".

Chat History:
{chat_history}

Current Question:
{question}

Return only the rewritten question.
""")

answer_chain = answer_prompt | llm
reformulation_chain = reformulation_prompt | llm

retriever = vector_store.as_retriever(
    search_kwargs={"k": 6}
)


def format_history(history):
    if not history:
        return "No previous conversation."

    lines = []

    for item in history[-6:]:
        lines.append(f"{item['role']}: {item['content']}")

    return "\n".join(lines)


def ask_question(question, history=None):
    chat_history = format_history(history)

    reformulated_question = reformulation_chain.invoke({
        "question": question,
        "chat_history": chat_history
    }).content.strip()

    docs = retriever.invoke(reformulated_question)

    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    response = answer_chain.invoke({
        "question": reformulated_question,
        "context": context,
        "chat_history": chat_history
    })

    return response.content
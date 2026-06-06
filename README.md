---
title: Agri Bot
emoji: 🌿
colorFrom: green
colorTo: blue
sdk: gradio
sdk_version: 5.0.0
python_version: 3.11
app_file: app.py
pinned: false
---


# Weed Management Assistant

A RAG-based chatbot that answers questions about weeds using information from a provided PDF guide.

## Features

- Reads weed management PDF
- Splits PDF content into small chunks
- Creates embeddings from chunks
- Stores embeddings in ChromaDB
- Retrieves relevant PDF context for user questions
- Answers only from the PDF context
- Supports follow-up questions using chat history
- Provides a simple chatbot UI using Gradio

## Project Structure

```text
agri_bot/
├── docs/
│   └── weeds.pdf
├── rag_engine.py
├── app.py
├── ui.py
├── .env
├── .gitignore
└── README.md

## RAG Pipeline

→ Text extraction
→ Chunking
→ Embeddings
→ ChromaDB
→ Retrieval
→ Prompt
→ LLM answer
# API-LLM
# LLM API

A FastAPI backend that exposes locally hosted language models via Ollama.  
Includes API key authentication, credit tracking with SQLite, and support for multiple models.

## Features
- FastAPI REST API
- API key authentication
- Credit-based usage tracking
- SQLite persistence
- Multiple LLM support (Gemma, LLaMA, Mistral)
- Runs fully locally with Ollama

## Tech Stack
- Python
- FastAPI
- SQLite
- Ollama
- Uvicorn

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn ollama pydantic python-dotenv
ollama pull gemma:2b
uvicorn main:app --reload

from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel
import ollama

from database import init_db, get_user, deduct_credit, add_user

app = FastAPI(title="Local LLM API")

SUPPORTED_MODELS = {
    "gemma": "gemma:2b",
    "llama": "llama3.2:1b",
    "mistral": "mistral:7b"
}

class GenerateRequest(BaseModel):
    prompt: str
    model: str = "gemma"

class GenerateResponse(BaseModel):
    response: str
    model_used: str
    remaining_credits: int

@app.on_event("startup")
def startup():
    init_db()
    add_user("testkey123", 5)

def verify_api_key(x_api_key: str = Header(...)):
    row = get_user(x_api_key)
    if not row:
        raise HTTPException(status_code=401, detail="Invalid API key")
    if row[0] <= 0:
        raise HTTPException(status_code=403, detail="No credits remaining")
    return x_api_key

def run_llm(prompt: str, model_short: str) -> str:
    if model_short not in SUPPORTED_MODELS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported model. Choose from {list(SUPPORTED_MODELS.keys())}"
        )

    result = ollama.chat(
        model=SUPPORTED_MODELS[model_short],
        messages=[{"role": "user", "content": prompt}]
    )
    return result["message"]["content"]

@app.post("/generate", response_model=GenerateResponse)
def generate(body: GenerateRequest, x_api_key: str = Depends(verify_api_key)):
    text = run_llm(body.prompt, body.model)
    deduct_credit(x_api_key)
    remaining = get_user(x_api_key)[0]

    return {
        "response": text,
        "model_used": body.model,
        "remaining_credits": remaining
    }

@app.get("/credits")
def credits(x_api_key: str = Depends(verify_api_key)):
    return {"remaining_credits": get_user(x_api_key)[0]}

@app.get("/models")
def models():
    return {"supported_models": list(SUPPORTED_MODELS.keys())}
from fastapi import FastAPI
from pydantic import BaseModel
from huggingface_hub import InferenceClient
import uvicorn

app = FastAPI()

HF_API_TOKEN = "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"
MODEL_NAME = "ibm-granite/granite-3.3-2b-instruct"
client = InferenceClient(model=MODEL_NAME, token=HF_API_TOKEN)

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str

@app.get("/")
def home():
    return {"message": "Finance Chatbot Backend is running 🚀"}

@app.post("/chat", response_model=QueryResponse)
def chat(req: QueryRequest):
    try:
        response = client.text_generation(
            prompt=req.query,
            max_new_tokens=300,
            temperature=0.7,
        )
        return {"response": response}
    except Exception as e:
        return {"response": f"❌ Error: {str(e)}"}

if _name_ == "_main_":
    uvicorn.run(app, host="127.0.0.1", port=8000)

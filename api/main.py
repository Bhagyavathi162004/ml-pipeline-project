from fastapi import FastAPI
from pydantic import BaseModel
from services.model_service import predict
from services.storage_service import save_data

app = FastAPI()

class UserInput(BaseModel):
    age: int
    session_duration: float
    pages_visited: int
    purchase_amount: float
    is_mobile: int

@app.get("/")
def home():
    return {"status": "running", "message": "ML API is LIVE 🚀"}

@app.post("/predict")
def make_prediction(data: UserInput):
    pred, prob = predict(data)

    result_text = "CHURN RISK" if pred == 1 else "SAFE USER"

    # 🔥 SAVE TO STORAGE
    save_data({
        "age": int(data.age),
        "prediction": result_text,
        "confidence": float(prob)
    })

    return {
        "success": True,
        "prediction": int(pred),
        "confidence": round(float(prob), 4),
        "result": result_text
    }
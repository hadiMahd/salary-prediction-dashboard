from fastapi import FastAPI

from app.api.db import router as db_router
from app.api.ollama_llm import router as ollama_router
from app.api.pred_llm_service import router as prediction_router

app = FastAPI(title="Salary Prediction API")


@app.get("/", tags=["api"])
async def health_check():
	return {"status": "ok", "service": "salary-prediction-api"}

app.include_router(db_router, prefix="/api")
app.include_router(prediction_router, prefix="/api")
app.include_router(ollama_router, prefix="/api")
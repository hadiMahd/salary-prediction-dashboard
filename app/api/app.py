import time
from fastapi import FastAPI, HTTPException
from models import PredictionInput, PredictionRecord, LLMAnalysis
from prediction_api import predict_salary  # You implement this
from llm_api import get_llm_analysis
#from database import save_prediction

app = FastAPI(title="Salary Prediction API")

@app.post("/predict")
async def predict( input: PredictionInput):
    start_time = time.time()
    
    try:
        # 1️⃣ ML Prediction
        predicted_salary = predict_salary(input.dict())
        
        # 2️⃣ LLM Analysis (uses your prompt.txt template)
        features = input.dict()
        llm_result: LLMAnalysis = get_llm_analysis(features, predicted_salary)
        
        # 3️⃣ Calculate latency
        latency_ms = round((time.time() - start_time) * 1000, 2)
        
        # 4️⃣ Build full record for Supabase
        record = PredictionRecord(
            **input.dict(),
            predicted_salary=predicted_salary,
            llm_narrative=llm_result.narrative,
            chart_data=llm_result.dict(),  # Full JSONB object
            inference_latency_ms=latency_ms
        )
        
        # 5️⃣ Save to Supabase
        save_prediction(record)
        
        # 6️⃣ Return to interface
        return {
            "predicted_salary": predicted_salary,
            "analysis": llm_result.dict(),
            "latency_ms": latency_ms
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline failed: {str(e)}")
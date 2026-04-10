import os
import time
import pickle
import pandas as pd
from google import genai
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException

from app.api.models import PredictionInput, PredictionRecord, SalaryAnalysis
from app.api.db import save_prediction_to_db

router = APIRouter(prefix="/prediction", tags=["api"])

load_dotenv()

# ─────────────────────────────────────────────────────────────
# 🔹 ML MODEL LOGIC (Exact feature order preserved)
# ─────────────────────────────────────────────────────────────

def load_ml_model():
    """Loads the pickle model safely."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, "..", "ml_model", "rf_salary_model.pkl")
    
    try:
        with open(model_path, "rb") as f:
            loaded_data = pickle.load(f)
        return loaded_data["model"], loaded_data["feature_names"]
    except FileNotFoundError:
        raise RuntimeError("Model file not found. Ensure ml_model/rf_salary_model.pkl exists.")
    except Exception as e:
        raise RuntimeError(f"Could not load model: {e}")

def prepare_ml_input(data: PredictionInput, trained_features):
    """
    Prepares dataframe for model prediction.
    ⚠️ Feature order matches your original code EXACTLY.
    """
    sample_input = {
        "work_year": data.work_year,           # 1
        "experience_level": data.experience_level,  # 2
        "employment_type": data.employment_type,    # 3
        "job_title": data.job_title,           # 4
        "remote_ratio": data.remote_ratio,     # 5
        "company_location": data.company_location,  # 6
        "company_size": data.company_size,     # 7
    }

    sample_df = pd.DataFrame([sample_input])
    sample_encoded = pd.get_dummies(sample_df)

    # Align columns with trained features (handles missing dummy columns)
    missing_cols = {col: 0 for col in trained_features if col not in sample_encoded.columns}
    sample_final = pd.concat([sample_encoded, pd.DataFrame([missing_cols])], axis=1)
    
    # 🔹 CRITICAL: Reorder columns to match trained_features EXACTLY
    sample_final = sample_final[trained_features]

    return sample_final

def get_ml_prediction(data: PredictionInput) -> float:
    """Orchestrates ML loading and prediction."""
    model, features = load_ml_model()
    input_df = prepare_ml_input(data, features)
    prediction = model.predict(input_df)
    return float(prediction[0])

# ─────────────────────────────────────────────────────────────
# 🔹 LLM LOGIC (Updated Prompt + Structured Output)
# ─────────────────────────────────────────────────────────────

def get_genai_client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set.")
    return genai.Client(api_key=api_key)

def get_llm_analysis(data: PredictionInput, predicted_salary: float) -> SalaryAnalysis:
    """
    Sends features + prediction to Gemini.
    Prompt asks Gemini to ESTIMATE market averages AND include predicted salary in chart.
    """
    # 📝 Updated Prompt: Includes predicted salary in chart_values
    prompt = f"""
Use the full input feature set below for salary reasoning.

Feature Input:
- work_year: {data.work_year}
- experience_level: {data.experience_level}
- employment_type: {data.employment_type}
- job_title: {data.job_title}
- remote_ratio: {data.remote_ratio}
- company_location: {data.company_location}
- company_size: {data.company_size}
- predicted_salary_usd: {predicted_salary:.2f}

Instructions:
1. Based on ALL features above, estimate realistic market average salaries (USD) for
   Entry, Mid, Senior, and Executive levels for this specific role/location/context.
2. Write exactly 2 sentences comparing the predicted salary to the market averages.
3. Return ONLY valid JSON matching the template below.
4. IMPORTANT: Include the Predicted Salary as the 5th value in chart_values.

Template:
{{
  "narrative": "...",
  "chart_title": "Salary Comparison",
  "chart_labels": ["Entry", "Mid", "Senior", "Executive", "Predicted"],
  "chart_values": [entry_avg, mid_avg, senior_avg, executive_avg, predicted_salary]
}}
"""

    try:
        client = get_genai_client()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_json_schema": SalaryAnalysis.model_json_schema(),
            },
        )
        return SalaryAnalysis.model_validate_json(response.text)
    except Exception as e:
        raise Exception(f"LLM Generation Failed: {str(e)}")

# ─────────────────────────────────────────────────────────────
# 🔹 COMBINED PROCESS FUNCTION (Latency Calculated Here)
# ─────────────────────────────────────────────────────────────

def process_prediction_pipeline(data: PredictionInput) -> dict:
    """
    Runs ML -> LLM and returns separate latency metrics.
    """
    ml_start_time = time.time()
    predicted_salary = get_ml_prediction(data)
    ml_latency_ms = round((time.time() - ml_start_time) * 1000, 2)

    llm_start_time = time.time()
    analysis = get_llm_analysis(data, predicted_salary)
    llm_latency_ms = round((time.time() - llm_start_time) * 1000, 2)

    return {
        "predicted_salary": predicted_salary,
        "analysis": analysis,
        "ml_inference_ms": ml_latency_ms,
        "llm_inference_latency_ms": llm_latency_ms,
        "total_inference_latency_ms": round(ml_latency_ms + llm_latency_ms, 2),
    }


@router.post("/test-ml")
async def test_ml_model_endpoint(input_data: PredictionInput):
    """Runs only the ML model (no Gemini, no DB write)."""
    try:
        start_time = time.time()
        predicted_salary = get_ml_prediction(input_data)
        latency_ms = round((time.time() - start_time) * 1000, 2)
        return {
            "status": "success",
            "predicted_salary": predicted_salary,
            "ml_inference_ms": latency_ms,
            "component": "ml-model",
        }
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="ML model not found.")
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"ML test failed: {str(exc)}")


@router.get("/test-gemini")
async def test_gemini_connection_endpoint():
    """Checks Gemini connectivity with a simple one-sentence prompt."""
    try:
        start_time = time.time()
        client = get_genai_client()
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents="Tell me a joke in one sentence.",
        )
        latency_ms = round((time.time() - start_time) * 1000, 2)
        return {
            "status": "success",
            "component": "gemini",
            "prompt": "Tell me a joke in one sentence.",
            "response": (response.text or "").strip(),
            "llm_inference_latency_ms": latency_ms,
        }
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Gemini connection test failed: {str(exc)}")


@router.post("/predict")
async def predict_endpoint(input_data: PredictionInput):
    try:
        result = process_prediction_pipeline(input_data)

        db_record = PredictionRecord(
            work_year=input_data.work_year,
            experience_level=input_data.experience_level,
            employment_type=input_data.employment_type,
            job_title=input_data.job_title,
            company_size=input_data.company_size,
            remote_ratio=input_data.remote_ratio,
            company_location=input_data.company_location[:10],
            predicted_salary=result["predicted_salary"],
            llm_narrative=result["analysis"].narrative,
            chart_data=result["analysis"].model_dump(),
            ml_inference_ms=result["ml_inference_ms"],
            llm_inference_latency_ms=result["llm_inference_latency_ms"],
            total_inference_latency_ms=result["total_inference_latency_ms"],
        )

        save_prediction_to_db(db_record.model_dump())

        return {
            "status": "success",
            "predicted_salary": result["predicted_salary"],
            "analysis": result["analysis"].model_dump(),
            "ml_inference_ms": result["ml_inference_ms"],
            "llm_inference_latency_ms": result["llm_inference_latency_ms"],
            "total_inference_latency_ms": result["total_inference_latency_ms"],
        }

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="ML model not found.")
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
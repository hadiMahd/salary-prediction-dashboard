import os
import time
import json

from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv
from ollama import Client  # type: ignore[import-not-found]

from app.api.db import save_prediction_to_db
from app.api.models import PredictionInput, PredictionRecord, SalaryAnalysis
from app.api.pred_llm_service import get_ml_prediction
from ...utils import limiter  # Import the shared limiter instance


load_dotenv()

router = APIRouter(prefix="/ollama", tags=["api"])


@router.get("/test")
async def test_ollama_endpoint():
	"""Simple Ollama connectivity test endpoint."""
	try:
		api_key = os.getenv("OLLAMA_API_KEY")
		if not api_key:
			raise HTTPException(
				status_code=500,
				detail="OLLAMA_API_KEY is not set. Create one at ollama.com/settings/keys.",
			)

		model_name = os.getenv("OLLAMA_CLOUD_MODEL", "glm-5.1:cloud")
		client = Client(
			host="https://ollama.com",
			headers={"Authorization": f"Bearer {api_key}"},
		)

		response = client.chat(
			model=model_name,
			messages=[{"role": "user", "content": "Hello!"}],
		)
		return {
			"status": "success",
			"mode": "cloud",
			"model": model_name,
			"response": response.message.content,
		}
	except ImportError:
		raise HTTPException(
			status_code=500,
			detail="Package 'ollama' is not installed. Install it first.",
		)
	except HTTPException:
		raise
	except Exception as exc:
		raise HTTPException(status_code=500, detail=f"Ollama test failed: {str(exc)}")


def get_ollama_client() -> Client:
	api_key = os.getenv("OLLAMA_API_KEY")
	if not api_key:
		raise RuntimeError("OLLAMA_API_KEY is not set. Create one at ollama.com/settings/keys.")

	return Client(
		host="https://ollama.com",
		headers={"Authorization": f"Bearer {api_key}"},
	)


def get_ollama_analysis(data: PredictionInput, predicted_salary: float) -> SalaryAnalysis:
	model_name = os.getenv("OLLAMA_CLOUD_MODEL", "glm-5.1:cloud")
	client = get_ollama_client()

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
3. Return ONLY valid JSON with keys:
   narrative, chart_title, chart_labels, chart_values
4. chart_labels must be: ["Entry", "Mid", "Senior", "Executive", "Predicted"]
5. chart_values must include 5 numeric values where the last value is predicted salary.
"""

	response = client.chat(
		model=model_name,
		messages=[{"role": "user", "content": prompt}],
		format=SalaryAnalysis.model_json_schema(),
	)

	raw_content = (response.message.content or "").strip()
	try:
		return SalaryAnalysis.model_validate_json(raw_content)
	except Exception:
		# Some models may wrap JSON in text. Try best-effort extraction.
		start = raw_content.find("{")
		end = raw_content.rfind("}")
		if start == -1 or end == -1 or end <= start:
			raise RuntimeError("Ollama response did not contain valid JSON payload.")
		json_payload = raw_content[start : end + 1]
		return SalaryAnalysis.model_validate(json.loads(json_payload))


def process_ollama_prediction_pipeline(data: PredictionInput) -> dict:
	ml_start_time = time.time()
	predicted_salary = get_ml_prediction(data)
	ml_latency_ms = round((time.time() - ml_start_time) * 1000, 2)

	llm_start_time = time.time()
	analysis = get_ollama_analysis(data, predicted_salary)
	llm_latency_ms = round((time.time() - llm_start_time) * 1000, 2)

	return {
		"predicted_salary": predicted_salary,
		"analysis": analysis,
		"ml_inference_ms": ml_latency_ms,
		"llm_inference_latency_ms": llm_latency_ms,
		"total_inference_latency_ms": round(ml_latency_ms + llm_latency_ms, 2),
	}


@router.post("/predict-insights")
@limiter.limit("10/minute")  # Apply rate limiting to this endpoint
async def predict_with_ollama_insights_endpoint(input_data: PredictionInput):
	"""Runs ML + Ollama insights and saves the full record in DB."""
	try:
		result = process_ollama_prediction_pipeline(input_data)

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
			"provider": "ollama-cloud",
			"model": os.getenv("OLLAMA_CLOUD_MODEL", "glm-5.1:cloud"),
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
		raise HTTPException(status_code=500, detail=f"Ollama insights pipeline failed: {str(exc)}")

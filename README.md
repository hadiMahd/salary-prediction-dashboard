# Salary Prediction API (ML + Ollama Cloud)

## Overview
This project predicts salary with a local ML model and generates insights using Ollama Cloud.
Each prediction is stored in Supabase with separate latency metrics for ML, LLM, and total pipeline time.

## Architecture
- FastAPI app entry: `main.py`
- Routers:
	- `app/api/ollama_llm.py` (primary workflow)
	- `app/api/db.py` (DB connectivity + inserts)
	- `app/api/pred_llm_service.py` (secondary Gemini path)
- Database: Supabase table `predictions`

## Primary Workflow (Ollama Cloud)
1. Validate input payload.
2. Run ML model inference.
3. Send features + predicted salary to Ollama Cloud.
4. Parse structured insight output.
5. Save record to Supabase.
6. Return prediction, insights, and latency metrics.

## API Endpoints
- `GET /` (health)
- `GET /api/db/test-connection`
- `GET /api/ollama/test`
- `POST /api/ollama/predict-insights`
- `GET /docs`

## Latency Fields
- `ml_inference_ms`: local ML inference time
- `llm_inference_latency_ms`: Ollama Cloud inference time
- `total_inference_latency_ms`: ML + LLM total time

## Environment Variables
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `OLLAMA_API_KEY`
- `OLLAMA_CLOUD_MODEL` (optional, default: `glm-5.1:cloud`)

## Run
```bash
uv sync
uv run -m uvicorn main:app --reload --port 8000
```

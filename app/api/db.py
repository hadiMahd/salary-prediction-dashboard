from supabase import create_client
import os
from dotenv import load_dotenv
from fastapi import APIRouter

load_dotenv()

router = APIRouter(prefix="/db", tags=["api"])

def get_supabase_client():
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    if not supabase_url or not supabase_key:
        raise RuntimeError("SUPABASE_URL or SUPABASE_KEY is not set.")
    return create_client(supabase_url, supabase_key)

def test_db_connection():
    """Tests connection to Supabase by fetching a sample record."""
    try:
        supabase = get_supabase_client()
        response = supabase.table("predictions").select("*").limit(1).execute()
        if response.data:
            return {"status": "success", "data": response.data[0]}
        else:
            return {"status": "success", "data": None, "message": "No records found."}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.get("/test-connection")
async def test_db_connection_endpoint():
    """Swagger-friendly endpoint to validate Supabase connectivity."""
    return test_db_connection()

def save_prediction_to_db(record: dict) -> dict:
    """Inserts data into the 'predictions' table."""
    record = dict(record)

    # Ensure company_location fits VARCHAR(10) constraint
    record['company_location'] = record['company_location'][:10]

    # Map API key to the current DB schema column name.
    if record.get("inference_latency_ms") is not None and record.get("ml_inference_ms") is None:
        record["ml_inference_ms"] = record["inference_latency_ms"]
    record.pop("inference_latency_ms", None)

    if record.get("ml_inference_ms") is not None:
        ml_latency_ms = round(float(record["ml_inference_ms"]), 2)
        record["ml_inference_ms"] = min(ml_latency_ms, 99999999.99)

    # New column for LLM-only latency. Keeps insert safe on strict numeric schemas.
    if record.get("llm_inference_latency_ms") is not None:
        llm_latency_ms = round(float(record["llm_inference_latency_ms"]), 2)
        record["llm_inference_latency_ms"] = min(llm_latency_ms, 99999999.99)

    if record.get("total_inference_latency_ms") is not None:
        total_latency_ms = round(float(record["total_inference_latency_ms"]), 2)
        record["total_inference_latency_ms"] = min(total_latency_ms, 99999999.99)

    supabase = get_supabase_client()
    response = supabase.table("predictions").insert(record).execute()
    return response.data
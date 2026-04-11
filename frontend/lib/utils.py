import os
from datetime import datetime, timedelta
import pandas as pd
from supabase import create_client, Client

# Demo data for when Supabase is not available
DEMO_PREDICTIONS = [
    {
        "id": "1",
        "work_year": 2024,
        "experience_level": "SE",
        "employment_type": "FT",
        "job_title": "Senior Data Scientist",
        "company_size": "L",
        "remote_ratio": 50,
        "company_location": "US",
        "predicted_salary": 152000,
        "llm_narrative": "This senior data scientist position with a large company in North America earning $152,000 aligns perfectly with market averages. The salary matches the typical compensation for SE-level professionals in the market.",
        "chart_data": {
            "labels": ["Entry", "Mid", "Senior", "Executive"],
            "values": [62000, 98000, 152000, 225000]
        },
        "inference_latency_ms": 145.32,
        "created_at": (datetime.utcnow() - timedelta(days=1)).isoformat()
    },
    {
        "id": "2",
        "work_year": 2024,
        "experience_level": "MI",
        "employment_type": "FT",
        "job_title": "Machine Learning Engineer",
        "company_size": "L",
        "remote_ratio": 100,
        "company_location": "US",
        "predicted_salary": 125000,
        "llm_narrative": "This mid-level ML engineer role offers $125,000, which is above average for mid-career professionals. Remote flexibility adds significant value to the compensation package.",
        "chart_data": {
            "labels": ["Entry", "Mid", "Senior", "Executive"],
            "values": [62000, 98000, 152000, 225000]
        },
        "inference_latency_ms": 128.45,
        "created_at": (datetime.utcnow() - timedelta(days=2)).isoformat()
    },
    {
        "id": "3",
        "work_year": 2024,
        "experience_level": "EX",
        "employment_type": "FT",
        "job_title": "Director of Data Science",
        "company_size": "L",
        "remote_ratio": 0,
        "company_location": "US",
        "predicted_salary": 210000,
        "llm_narrative": "Executive-level compensation at $210,000 reflects the seniority and responsibility of a Director role. This is competitive within the executive salary range for tech companies.",
        "chart_data": {
            "labels": ["Entry", "Mid", "Senior", "Executive"],
            "values": [62000, 98000, 152000, 225000]
        },
        "inference_latency_ms": 156.78,
        "created_at": (datetime.utcnow() - timedelta(days=3)).isoformat()
    },
    {
        "id": "4",
        "work_year": 2024,
        "experience_level": "EN",
        "employment_type": "FT",
        "job_title": "Junior Data Analyst",
        "company_size": "M",
        "remote_ratio": 50,
        "company_location": "US",
        "predicted_salary": 65000,
        "llm_narrative": "Entry-level analyst position at $65,000 is slightly above the market entry average. Mid-sized company offers growth opportunities typical for junior professionals.",
        "chart_data": {
            "labels": ["Entry", "Mid", "Senior", "Executive"],
            "values": [62000, 98000, 152000, 225000]
        },
        "inference_latency_ms": 110.12,
        "created_at": (datetime.utcnow() - timedelta(days=4)).isoformat()
    }
]

DEMO_MODEL_PERFORMANCE = [
    {
        "id": "1",
        "model_version": "v1.0.0",
        "algorithm": "RandomForestRegressor",
        "r2_score": 0.892,
        "mae": 8500.50,
        "rmse": 12340.75,
        "feature_importance": {
            "experience_level": 0.35,
            "company_size": 0.22,
            "remote_ratio": 0.18,
            "employment_type": 0.15,
            "work_year": 0.10
        },
        "hyperparameters": {
            "n_estimators": 100,
            "max_depth": 15,
            "min_samples_split": 5
        },
        "training_date": (datetime.utcnow() - timedelta(days=7)).isoformat()
    },
    {
        "id": "2",
        "model_version": "v1.1.0",
        "algorithm": "RandomForestRegressor",
        "r2_score": 0.905,
        "mae": 7800.25,
        "rmse": 11200.50,
        "feature_importance": {
            "experience_level": 0.38,
            "company_size": 0.24,
            "remote_ratio": 0.16,
            "employment_type": 0.14,
            "work_year": 0.08
        },
        "hyperparameters": {
            "n_estimators": 150,
            "max_depth": 16,
            "min_samples_split": 4
        },
        "training_date": (datetime.utcnow() - timedelta(days=3)).isoformat()
    }
]


def get_supabase_client() -> Client:
    """Initialize Supabase client."""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if url and key:
        return create_client(url, key)
    return None


def fetch_predictions(use_demo: bool = False) -> pd.DataFrame:
    """Fetch predictions from Supabase or return demo data."""
    if use_demo:
        return pd.DataFrame(DEMO_PREDICTIONS)
    
    client = get_supabase_client()
    if client:
        try:
            response = client.table("predictions").select("*").execute()
            return pd.DataFrame(response.data)
        except Exception as e:
            print(f"Error fetching from Supabase: {e}")
            return pd.DataFrame(DEMO_PREDICTIONS)
    
    return pd.DataFrame(DEMO_PREDICTIONS)


def fetch_model_performance(use_demo: bool = False) -> pd.DataFrame:
    """Fetch model performance from Supabase or return demo data."""
    if use_demo:
        return pd.DataFrame(DEMO_MODEL_PERFORMANCE)
    
    client = get_supabase_client()
    if client:
        try:
            response = client.table("model_performance").select("*").execute()
            return pd.DataFrame(response.data)
        except Exception as e:
            print(f"Error fetching from Supabase: {e}")
            return pd.DataFrame(DEMO_MODEL_PERFORMANCE)
    
    return pd.DataFrame(DEMO_MODEL_PERFORMANCE)


def format_salary(salary: float) -> str:
    """Format salary as currency."""
    return f"${salary:,.0f}"


def format_percentage(value: float) -> str:
    """Format value as percentage."""
    return f"{value * 100:.1f}%"

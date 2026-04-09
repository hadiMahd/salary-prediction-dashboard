import pickle
import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()


class PredictionRequest(BaseModel):
    work_year: int = Field(example=2022)
    experience_level: str = Field(example="SE")
    employment_type: str = Field(example="FT")
    job_title: str = Field(example="Data Scientist")
    remote_ratio: int = Field(example=50)
    company_location: str = Field(example="US")
    company_size: str = Field(example="M")


class PredictionResponse(BaseModel):
    predicted_salary: float


def load_model():
    try:
        with open("app/ml_model/rf_salary_model.pkl", "rb") as f:
            loaded_data = pickle.load(f)
    except FileNotFoundError:
        raise
    except ModuleNotFoundError:
        raise
    except Exception as exc:
        raise RuntimeError(f"Could not load model: {exc}")

    try:
        loaded_model = loaded_data["model"]
        trained_features = loaded_data["feature_names"]
    except KeyError as exc:
        raise RuntimeError(f"Model pickle missing expected key: {exc}")

    return loaded_model, trained_features


def prepare_input(data: PredictionRequest, trained_features):
    sample_input = {
        "work_year": data.work_year,
        "experience_level": data.experience_level,
        "employment_type": data.employment_type,
        "job_title": data.job_title,
        "remote_ratio": data.remote_ratio,
        "company_location": data.company_location,
        "company_size": data.company_size,
    }

    sample_df = pd.DataFrame([sample_input])
    sample_encoded = pd.get_dummies(sample_df)

    missing_cols = {col: 0 for col in trained_features if col not in sample_encoded.columns}
    sample_final = pd.concat([sample_encoded, pd.DataFrame([missing_cols])], axis=1)
    sample_final = sample_final[trained_features]

    return sample_final


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict_salary(request: PredictionRequest):
    try:
        loaded_model, trained_features = load_model()
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Model file not found.")
    except ModuleNotFoundError:
        raise HTTPException(status_code=500, detail="Missing dependency: scikit-learn.")
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    try:
        sample_final = prepare_input(request, trained_features)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Input processing failed: {exc}")

    try:
        prediction = loaded_model.predict(sample_final)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {exc}")

    return PredictionResponse(predicted_salary=float(prediction[0]))

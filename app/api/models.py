from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from typing import Literal

# 🔹 Input: Matches 'predictions' table columns
class PredictionInput(BaseModel):
    work_year: int
    experience_level: str = Field(..., pattern="^(EN|MI|SE|EX)$")
    employment_type: str = Field(..., pattern="^(FT|PT|CT|FL)$")
    job_title: str
    company_size: str = Field(..., pattern="^(S|M|L)$")
    remote_ratio: Literal[0, 50, 100]
    company_location: str  # ⚠️ Keep short (VARCHAR(10) in DB)

# 🔹 LLM Output: Matches Supabase 'chart_data' JSONB structure
# This schema is passed to Gemini to force structured output
class SalaryAnalysis(BaseModel):
    narrative: str = Field(description="Exactly 2 sentences comparing predicted salary to market averages.")
    chart_title: str = Field(description="Title for the salary chart.")
    chart_labels: List[str] = Field(description="Fixed list: ['Entry', 'Mid', 'Senior', 'Executive']")
    chart_values: List[float] = Field(description="Estimated market averages in USD for each level.")

# 🔹 DB Record: Full object for Supabase insert
class PredictionRecord(BaseModel):
    work_year: int
    experience_level: str
    employment_type: str
    job_title: str
    company_size: str
    remote_ratio: int
    company_location: str
    predicted_salary: float
    llm_narrative: str
    chart_data: Dict[str, Any]
    ml_inference_ms: Optional[float] = None
    llm_inference_latency_ms: Optional[float] = None
    total_inference_latency_ms: Optional[float] = None
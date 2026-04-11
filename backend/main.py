from fastapi import FastAPI, Request

from app.api.db import router as db_router
from app.api.ollama_llm import router as ollama_router
from app.api.pred_llm_service import router as prediction_router
from utils import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

app = FastAPI(title="Salary Prediction API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

@app.get("/", tags=["api"])
@limiter.limit("3/minute")  # Apply rate limiting to the health check endpoint
async def health_check(request: Request):
	return {"status": "ok", "service": "salary-prediction-api"}

app.include_router(db_router, prefix="/api")
app.include_router(prediction_router, prefix="/api")
app.include_router(ollama_router, prefix="/api")
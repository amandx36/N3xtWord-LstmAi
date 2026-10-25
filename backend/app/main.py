
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .predictNextWord import load_artifacts, predict_next_word
from .requestFormat import PredictionRequest


app = FastAPI(
    title="Next Word Prediction API",
    description="predict the next word using trained lstm model ",
    version="1.0.0",
)

origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS", "http://localhost:3000,http://localhost:8000"
    ).split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"]
)

model_load_error: str | None = None


@app.on_event("startup")
def startup() -> None:
    global model_load_error
    try:
        load_artifacts()
        model_load_error = None
    except RuntimeError as exc:
        # Keep health/status routes available so a missing artifact is diagnosable.
        model_load_error = str(exc)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Next Word Prediction API", "version": app.version}


@app.get("/health")
def health() -> dict[str, str | bool | None]:
    ready = model_load_error is None
    return {
        "status": "ok" if ready else "degraded",
        "model_loaded": ready,
        "detail": model_load_error,
    }


@app.post("/predict")
def predict(request: PredictionRequest) -> dict[str, object]:
    predictions = predict_next_word(request.text, request.top_k)
    response: dict[str, object] = {
        "input": request.text,
        "predictions": predictions,
    }
    if predictions:
        response["predicted_word"] = predictions[0]["word"]
        response["confidence"] = predictions[0]["probability"]
    return response

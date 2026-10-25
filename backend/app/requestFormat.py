from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    """Validated input accepted by the prediction endpoint."""

    text: str = Field(min_length=1, max_length=5000)
    top_k: int = Field(default=3, ge=1, le=10)

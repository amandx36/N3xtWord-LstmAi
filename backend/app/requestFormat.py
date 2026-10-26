from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    #  input accepted by the prediction end point 

    text: str = Field(min_length=1, max_length=5000)
    top_k: int = Field(default=3, ge=1, le=10)

import json 
import re 
from pathlib import Path 

from fastapi import FastAPI
import numpy as np 
import tensorflow as tf 

app = FastAPI(title="Next word prediction Api  using lstm model ", description="Backend api for predicting the next word",version="1.0.0")

# adding the cors 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    
    allow_methods=["GET","POST"],
    allow_headers=["*"]
)

@app.get("/")
async def root():
    return {
        "message": "Welcome to the next word prediction api using lstm model ",
        "version": "1.0.0"
    }

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "message": "API is healthy"
    }

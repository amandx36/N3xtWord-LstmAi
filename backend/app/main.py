import json 
import re 
from pathlib import Path 
import os 
from fastapi import FastAPI
import numpy as np 
import tensorflow as tf 
from dotenv import load_dotenv

MODEL_PATH = os.getenv("MODEL_PATH")
VOCAB_PATH =  os.getenv("VOCAB_PATH")


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

# load the trained model 

@app.on_event("startup")
def load_model():

    global model, word_to_id, id_to_word

    if not MODEL_PATH.exists():
        raise RuntimeError(
            f"Model not found: {MODEL_PATH}"
        )

    if not VOCAB_PATH.exists():
        raise RuntimeError(
            f"Vocabulary not found: {VOCAB_PATH}"
        )

    # Load the trained LSTM model
    model = tf.keras.models.load_model(
        MODEL_PATH,
        compile=False
    )

    # Load the vocabulary used during training
    with open(VOCAB_PATH, "r", encoding="utf-8") as file:
        vocabulary = json.load(file)

    word_to_id = vocabulary["word_to_id"]

    id_to_word = {
        int(token_id): word
        for token_id, word
        in vocabulary["id_to_word"].items()
    }

    print("LSTM model loaded successfully!")
    print("Vocabulary loaded successfully!")


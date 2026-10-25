"""Model loading and inference for the notebook's LSTM architecture."""

import json
import os
import re
from pathlib import Path
from typing import Any

import numpy as np
import tensorflow as tf
from fastapi import HTTPException


APP_DIR = Path(__file__).resolve().parent
MODEL_PATH = Path(os.getenv("MODEL_PATH", APP_DIR / "artifacts" / "lstm_model.keras"))
VOCAB_PATH = Path(os.getenv("VOCAB_PATH", APP_DIR / "artifacts" / "vocabulary.json"))
SEQ_LEN = int(os.getenv("SEQ_LEN", "30"))
PAD_TOKEN = os.getenv("PAD_TOKEN", "<PAD>")
UNK_TOKEN = os.getenv("UNK_TOKEN", "<UNK>")

model: Any | None = None
word_to_id: dict[str, int] = {}
id_to_word: dict[int, str] = {}


def load_artifacts() -> None:
    #  load the model and vocabilary 
    global model, word_to_id, id_to_word

    missing = [str(path) for path in (MODEL_PATH, VOCAB_PATH) if not path.is_file()]
    if missing:
        raise RuntimeError(
            "Required model artifacts are missing: " + ", ".join(missing)
            + "model and vocabilary is required "
        )

    try:
        with VOCAB_PATH.open("r", encoding="utf-8") as file:
            vocabulary = json.load(file)
        loaded_word_to_id = {str(word): int(token_id) for word, token_id in vocabulary["word_to_id"].items()}
        loaded_id_to_word = {
            int(token_id): str(word)
            for token_id, word in vocabulary["id_to_word"].items()
        }
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        raise RuntimeError(f"Could not read vocabulary at {VOCAB_PATH}: {exc}") from exc

    if PAD_TOKEN not in loaded_word_to_id or UNK_TOKEN not in loaded_word_to_id:
        raise RuntimeError(f"Vocabulary must contain {PAD_TOKEN} and {UNK_TOKEN} tokens")

    loaded_model = tf.keras.models.load_model(MODEL_PATH, compile=False)
    model = loaded_model
    word_to_id = loaded_word_to_id
    id_to_word = loaded_id_to_word


def clean_text(text: str) -> str:
    """Apply the same WikiText cleanup used before training in the notebook."""
    text = text.replace("@-@", "-").replace("@,@", ",").replace("@.@", ".")
    text = re.sub(r"=+\s*(.*?)\s*=+", r"\1", text)
    return re.sub(r"\s+", " ", text).strip()


def tokenize(text: str) -> list[str]:
    # Matches notebook cell 16: lowercase word tokens, retaining contractions.
    return re.findall(r"\b\w+(?:['’]\w+)*\b", clean_text(text).lower())


def predict_next_word(text: str, top_k: int = 3) -> list[dict[str, float | str]]:
    if model is None:
        raise HTTPException(status_code=503, detail="Prediction model is not loaded")

    words = tokenize(text)
    if not words:
        raise HTTPException(status_code=422, detail="Text must contain at least one word")

    unknown_id = word_to_id[UNK_TOKEN]
    token_ids = [word_to_id.get(word, unknown_id) for word in words][-SEQ_LEN:]
    pad_id = word_to_id[PAD_TOKEN]
    token_ids = [pad_id] * (SEQ_LEN - len(token_ids)) + token_ids

    probabilities = np.asarray(model.predict(np.asarray([token_ids], dtype=np.int32), verbose=0))
    if probabilities.ndim != 2 or probabilities.shape[0] != 1:
        raise HTTPException(status_code=500, detail="Model returned an unexpected prediction shape")
    probabilities = probabilities[0]
    if not np.all(np.isfinite(probabilities)):
        raise HTTPException(status_code=500, detail="Model returned invalid prediction scores")

    results: list[dict[str, float | str]] = []
    for token_id in np.argsort(probabilities)[::-1]:
        word = id_to_word.get(int(token_id), UNK_TOKEN)
        if word in {PAD_TOKEN, UNK_TOKEN}:
            continue
        results.append({"word": word, "probability": round(float(probabilities[token_id]), 6)})
        if len(results) == top_k:
            break
    return results

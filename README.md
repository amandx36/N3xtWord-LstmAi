# NextWord AI

NextWord AI is a full-stack next-word prediction demo. Enter a sentence in the web interface and the application uses a trained LSTM language model to suggest likely continuations. Suggestions can be clicked to add them to the text and continue experimenting.

The project pairs a Next.js and TypeScript frontend with a FastAPI inference service. The model expects up to 30 tokens and returns ranked candidates with their model probabilities. Those probabilities are scores from the model, not calibrated guarantees of correctness.

## Features

- Interactive text input with automatic predictions as you type
- Adjustable number of suggestions (up to 10)
- Click a suggestion to append it to the input
- FastAPI endpoints for prediction and service health
- Docker Compose configuration for running both services together
- Notebook containing the model development workflow

## Architecture

```text
Browser → Next.js frontend (:3000) → FastAPI (:8000)
                                      ├── Keras model
                                      └── Vocabulary
```

The browser calls Next.js route handlers at `/api/predict` and `/api/health`. Those handlers proxy requests to FastAPI, using `N3xtharBackendUrl` as the backend base URL. The API loads the model and vocabulary once when it starts.

## Repository layout

| Path | Purpose |
| --- | --- |
| `frontendlstm/` | Next.js App Router application and API proxy routes |
| `backend/app/` | FastAPI application, request schema, and prediction logic |
| `backend/app/artifacts/` | Keras model and vocabulary required for inference |
| `NextWordPredictor.ipynb` | Notebook used to develop and train the LSTM |
| `docker-compose.yml` | Local multi-container setup |
| `PRD.md` | Product requirements and planned product direction |

## Requirements

- Docker Engine with the Docker Compose plugin, for the container setup; or
- Python 3.12+ and Node.js 22+ for running each service directly

The checked-in model artifact is approximately 142 MB. Ensure it is present at `backend/app/artifacts/lstm_model.keras` along with `vocabulary.json` before starting the backend. The vocabulary file is tracked; the model file is ignored by `.gitignore`, so a fresh clone may need the model copied from your artifact storage or training output.

## Run with Docker Compose

Compose expects these two environment files (both are git-ignored):

- `frontendlstm/.env`
- `backend/app/.env`

Create `frontendlstm/.env` containing:

```dotenv
N3xtharBackendUrl=http://localhost:8000
```

And create `backend/app/.env` containing:

```dotenv
SEQ_LEN=30
PAD_TOKEN=<PAD>
UNK_TOKEN=<UNK>
```

Start both services from the repository root:

```sh
docker compose up --build
```

Open [http://localhost:3000](http://localhost:3000). The API is available at [http://localhost:8000](http://localhost:8000), with interactive documentation at [http://localhost:8000/docs](http://localhost:8000/docs).

The frontend container overrides `N3xtharBackendUrl` to `http://backend:8000` so it can reach the API over the Compose network. The Dockerfiles currently start the frontend in Next.js development mode.

## Run locally without Docker

### 1. Start the API

From the repository root:

```sh
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
pip install -r backend/requirement.txt
uvicorn app.main:app --app-dir backend --reload --host 0.0.0.0 --port 8000
```

The API reads these optional environment variables. Defaults point to the checked-in artifact locations relative to `backend/app/`.

| Variable | Default | Meaning |
| --- | --- | --- |
| `MODEL_PATH` | `backend/app/artifacts/lstm_model.keras` | Keras model path |
| `VOCAB_PATH` | `backend/app/artifacts/vocabulary.json` | Vocabulary JSON path |
| `SEQ_LEN` | `30` | Input sequence length |
| `PAD_TOKEN` | `<PAD>` | Vocabulary padding token |
| `UNK_TOKEN` | `<UNK>` | Vocabulary unknown-word token |
| `CORS_ORIGINS` | `http://localhost:3000,http://localhost:8000` | Comma-separated allowed origins |

### 2. Start the frontend

In a second terminal:

```sh
cd frontendlstm
npm ci
npm run dev
```

The frontend defaults its server-side API proxy to `http://127.0.0.1:8000`. To change it, set `N3xtharBackendUrl` in `frontendlstm/.env.local`, for example:

```dotenv
N3xtharBackendUrl=http://127.0.0.1:8000
```

Visit [http://localhost:3000](http://localhost:3000).

## API

### `GET /health`

Reports whether the API loaded the model and vocabulary. A missing or invalid artifact leaves the health route available with a degraded status.

```json
{
  "status": "ok",
  "model_loaded": true,
  "detail": null
}
```

### `POST /predict`

Request:

```json
{
  "text": "The future of artificial intelligence",
  "top_k": 3
}
```

`text` must contain 1–5000 characters. `top_k` is optional and defaults to 3; valid values are 1–10. The response includes the ranked `predictions` array and, when predictions are available, the top `predicted_word` and its `confidence` (the top candidate probability).

```json
{
  "input": "The future of artificial intelligence",
  "predictions": [
    { "word": "...", "probability": 0.0 }
  ],
  "predicted_word": "...",
  "confidence": 0.0
}
```

The values above are illustrative. The API cleans and tokenizes text, maps out-of-vocabulary words to `<UNK>`, keeps the most recent 30 tokens, pads on the left with `<PAD>`, and filters `<PAD>` and `<UNK>` from suggestions.

The frontend provides equivalent proxy routes at `GET /api/health` and `POST /api/predict`.

## Model and limitations

The notebook defines an embedding followed by two 128-unit LSTM layers, dropout, and a softmax output over the vocabulary. The inference service uses the saved model and `vocabulary.json`; preprocessing in the API is intended to match the notebook's WikiText cleanup and tokenization.

This is an experimental LSTM model trained for next-token prediction. It can produce repetitive, contextually weak, or incorrect suggestions and should not be treated as a modern general-purpose writing assistant. The PRD describes intended product work; routes and capabilities in this README reflect the current implementation. No evaluation metrics are claimed here because verified results are not part of the checked-in inference service.

## Development commands

From `frontendlstm/`:

```sh
npm run dev
npm run lint
npm run build
```

The FastAPI interactive API docs are served at `/docs` while the backend is running. The repository does not currently include a dedicated automated test suite.

## Troubleshooting

- **Health reports `degraded`:** Check that `MODEL_PATH` and `VOCAB_PATH` refer to readable files, and that the vocabulary contains `<PAD>` and `<UNK>`.
- **Predictions return 503:** The model did not load. Check backend startup output and verify the model artifact is compatible with the installed TensorFlow version.
- **Frontend cannot reach the API:** Confirm the backend is running and that `N3xtharBackendUrl` is reachable from the frontend process. With Compose, the frontend uses `http://backend:8000` internally.
- **Compose cannot find an env file:** Create `frontendlstm/.env` and `backend/app/.env` as described above.

## License

under  construction 

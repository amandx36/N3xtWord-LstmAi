import os
from pathlib import Path

from huggingface_hub import hf_hub_download

# Hugging Face repository
REPO_ID = "amandx360/lstmN3xwordPredictor"

# Save files inside backend/app/artifacts/
BASE_DIR = Path(__file__).resolve().parent
ARTIFACTS_DIR = BASE_DIR / "app" / "artifacts"

ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

FILES = [
    "lstm_model.keras",
    "vocabulary.json",
]


def download_files():
    print(f"Downloading model artifacts from Hugging Face: {REPO_ID}")

    for filename in FILES:
        print(f"Downloading {filename}...")

        downloaded_path = hf_hub_download(
            repo_id=REPO_ID,
            filename=filename,
            repo_type="model",
            local_dir=str(ARTIFACTS_DIR),
        )

        print(f"Downloaded successfully: {downloaded_path}")

    print("\nAll model artifacts are ready!")
    print(f"Artifacts directory: {ARTIFACTS_DIR}")


if __name__ == "__main__":
    download_files()

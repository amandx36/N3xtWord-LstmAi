import os
from pathlib import Path

from huggingface_hub import hf_hub_download

REPO_ID = "amandx360/lstmN3xwordPredictor"

# Docker container path
ARTIFACTS_DIR = Path(
    os.environ.get("ARTIFACTS_DIR", "/app/artifacts")
)
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

FILES = [
    "lstm_model.keras",
    "vocabulary.json",
]


def download_files():
    print(f"Downloading artifacts from Hugging Face: {REPO_ID}")
    print(f"Destination: {ARTIFACTS_DIR}")

    for filename in FILES:
        print(f"Downloading {filename}...")

        downloaded_path = hf_hub_download(
            repo_id=REPO_ID,
            filename=filename,
            repo_type="model",
            local_dir=str(ARTIFACTS_DIR),
        )

        print(f"Downloaded: {downloaded_path}")

        if not Path(downloaded_path).is_file():
            raise FileNotFoundError(
                f"Download failed: {downloaded_path}"
            )

    for filename in FILES:
        path = ARTIFACTS_DIR / filename
        if not path.is_file():
            raise FileNotFoundError(f"Missing artifact: {path}")

        print(f"Verified: {path} ({path.stat().st_size:,} bytes)")

    print("All model artifacts downloaded successfully.")


if __name__ == "__main__":
    download_files()

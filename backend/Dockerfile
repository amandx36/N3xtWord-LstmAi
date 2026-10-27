FROM python:3.12-slim

WORKDIR /app

ENV ARTIFACTS_DIR=/app/artifacts

COPY requirement.txt .

RUN python -m pip install --no-cache-dir \
    --retries 10 \
    --timeout 120 \
    -r requirement.txt

COPY . .

# Download the model and vocabulary during image build
RUN python downloadModelAndVoc.py

# Fail the build if either artifact is missing
RUN test -f /app/artifacts/lstm_model.keras \
    && test -f /app/artifacts/vocabulary.json \
    && ls -lh /app/artifacts/

EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]

FROM python:3.12-slim

WORKDIR /app

COPY requirement.txt .

# Retry interrupted package downloads
RUN python -m pip install --no-cache-dir \
    --retries 10 \
    --timeout 120 \
    -r requirement.txt

COPY . .

RUN python downloadModelAndVoc.py

EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]

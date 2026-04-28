FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
COPY README.md .

RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

COPY src/ /app/src/
COPY data /app/data

RUN pip install --no-cache-dir .

EXPOSE 8000
ENV PYTHONPATH=/app

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
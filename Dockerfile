FROM python:3.11-slim

WORKDIR /app

# Instala dependências do sistema necessárias para compilar algumas libs (como lz4 ou psutil)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de configuração
COPY pyproject.toml .

# Instala as dependências
RUN pip install --no-cache-dir .

# Copia o restante do código
COPY src/ /app/src/
COPY data/ /app/data/

EXPOSE 8000

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
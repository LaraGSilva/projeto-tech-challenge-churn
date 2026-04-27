# Variáveis para facilitar mudanças
IMAGE_NAME=churn-api
CONTAINER_PORT=8000

.PHONY: install lint test run docker-build docker-run help

# Instala as dependências necessárias
install:
	pip install -r requirements.txt

# Roda o Ruff para garantir a qualidade do código
lint:
	ruff check src/

# Executa os testes unitários e de fumaça
test:
	python -m pytest

# Roda a API localmente (fora do Docker)
run:
	uvicorn src.app:app --reload --port $(CONTAINER_PORT)

# Processa a ingestão e o batch
process-data:
	python src/ingest.py
	python src/motor_batch.py

# Docker: Constrói a imagem
docker-build:
	docker build -t $(IMAGE_NAME) .

# Docker: Sobe o container
docker-run:
	docker run -p $(CONTAINER_PORT):$(CONTAINER_PORT) $(IMAGE_NAME)

# Limpa arquivos temporários (pycache, etc)
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .ruff_cache

help:
	@echo "Comandos disponíveis:"
	@echo "  make lint         - Roda o linter Ruff"
	@echo "  make test         - Executa os testes com Pytest"
	@echo "  make docker-build - Cria a imagem Docker"
	@echo "  make docker-run   - Sobe a API no Docker"




	.PHONY: train report register

train:
	python -m src.train

report:
	python scripts/export_runs.py
	@echo "Resultados exportados para docs/results.md"

register:
	python -m src.register_model
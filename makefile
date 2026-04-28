# Variáveis para facilitar mudanças
IMAGE_NAME=churn-api
CONTAINER_PORT=8000
PYTHON_EXEC=python3
POETRY = python -m poetry

.PHONY: install lint test run process-data train docker-build docker-run clean help

# Instala as dependências usando Poetry
install:
	poetry install

# Roda o Ruff para garantir a qualidade do código na pasta src e tests
lint:
	poetry run ruff check src/ tests/

# Executa os testes unitários e de integração
test:
	poetry run pytest

# Roda a API localmente via uvicorn
run:
	poetry run uvicorn src.app:app --reload --port $(CONTAINER_PORT)

# Executa o pipeline de dados (Ingestão -> Pré-processamento -> treino -> Processamento em Lote)
process-data:
	poetry run python src/ingest.py
	poetry run python src/preprocess.py
	poetry run python src/train.py
	poetry run python src/motor_batch.py

# Executa o treinamento do modelo
train:
	poetry run python src/train.py

# Docker: Constrói a imagem
docker-build:
	docker build -t $(IMAGE_NAME) .

# Docker: Sobe o container
docker-run:
	docker run -p $(CONTAINER_PORT):$(CONTAINER_PORT) $(IMAGE_NAME)

# Limpa arquivos temporários e logs
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf mlruns/

help:
	@echo "Comandos disponíveis:"
	@echo "  make install      			- Instala dependências via Poetry"
	@echo "  make lint         			- Roda o linter Ruff"
	@echo "  make test         			- Executa os testes com Pytest"
	@echo "  make run          			- Inicia a API localmente"
	@echo "  make process-data 			- Roda o pipeline completo de dados"
	@echo "  make docker-build 			- Cria a imagem Docker"
	@echo "  make docker-run   			- Sobe a API no Docker"
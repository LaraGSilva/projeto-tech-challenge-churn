# 📊 Tech Challenge | Modelo Preditivo de Churn

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![MLflow](https://img.shields.io/badge/MLflow-3.3.2-orange.svg)](https://mlflow.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)](https://pytorch.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Projeto de Machine Learning para predição de churn em operadora de telecomunicações usando rede neural MLP (PyTorch) com pipeline completo de MLOps.

## 🎯 Objetivo
Desenvolver um modelo de classificação binária para identificar clientes com alto risco de cancelamento, permitindo intervenções proativas da equipe de CRM e Marketing.

## 🔄 Fluxo de Trabalho (End-to-End)

O diagrama abaixo ilustra o ciclo de vida dos dados, desde a ingestão até a disponibilização dos insights via API.

![fluxo mermaid](./docs/imgs/mermaid-diagram-simples.png)

[Para ter mais detalhes sobre a arquitetura, acesse nossa seção: ](arquitetura.md)

## 🏗️ Organização do repositório
```
projeto-tech-challenge-churn/
├── data/
│   ├── raw/                 # Dados brutos (Telco_customer_churn.xlsx)
│   └── processed/           # Dados tratados (dataset_tratado.parquet)
├── docs/                    # Documentação e Model Canvas
│   ├── model_canvas_business.md
│   └── imgs/               # Visualizações do projeto
├── models/                  # Modelos treinados
│   └── best_mlp_model.pt   # Melhor modelo MLP salvo
├── notebooks/              # Análises exploratórias
│   ├── EDA.ipynb          # Análise exploratória completa
│   ├── modelos_baseline.ipynb  # Comparação de baselines
│   └── modelo_mlp.ipynb   # Desenvolvimento do modelo MLP
├── src/                    # Código fonte modular
│   ├── preprocessing.py   # Carregamento e split dos dados
│   ├── pipeline.py        # Construção do pipeline sklearn
│   ├── train.py           # Treinamento com MLflow tracking
│   ├── evaluate.py        # Métricas e visualizações
│   └── utils.py           # Funções auxiliares
├── tests/                  # Testes automatizados (pytest)
├── main.py                 # Ponto de entrada (vazio)
├── requirements.txt        # Dependências Python
├── pyproject.toml         # Configuração do projeto
└── README.md
```


## 🛠️ Como Executar o Projeto

### 1. Pré-requisitos
```bash
# Python 3.8+ instalado
python --version

# Git (opcional, para clonar)
git --version
```

### 2. Clonagem e Setup
```bash
# Clone o repositório
git clone https://github.com/seu-usuario/projeto-tech-challenge-churn.git
cd projeto-tech-challenge-churn

# Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instale dependências
pip install -r requirements.txt
```

### 3. Execução da Análise Exploratória
```bash
# Abra Jupyter e execute os notebooks em ordem:
jupyter notebook

# 1. notebooks/EDA.ipynb - Análise completa dos dados
# 2. notebooks/modelos_baseline.ipynb - Comparação de baselines
# 3. notebooks/modelo_mlp.ipynb - Desenvolvimento do modelo MLP
```

### 4. Treinamento do Modelo
```bash
# Execute o treinamento com MLflow
python -c "
from src.preprocessing import load_and_split_data
from src.pipeline import get_mlp_pipeline
from src.train import run_training
from src.evaluate import evaluate_model

# Carregar dados
X_train, X_test, y_train, y_test = load_and_split_data()

# Criar pipeline
pipeline = get_mlp_pipeline()

# Treinar modelo
model = run_training(X_train, y_train, pipeline, 'MLP_Churn_Prediction')

# Avaliar
evaluate_model(model, X_test, y_test)
"
```

### 5. Visualizar Resultados no MLflow
```bash
# Inicie o servidor MLflow
mlflow ui

# Acesse http://localhost:5000
```

## 🔸 Funcionalidades

- ✅ **Pipeline completo:** Pré-processamento → Treinamento → Avaliação
- ✅ **Tracking com MLflow:** Experimentos, métricas e artefatos
- ✅ **Modelos baseline:** Comparação com Random Forest, Logistic Regression
- ✅ **Rede Neural MLP:** Implementação em PyTorch
- ✅ **Análise exploratória:** EDA completa com visualizações
- ✅ **Documentação:** Model Canvas com impacto de negócio


##  🔸 Model canvas business
[Para ter mais detalhes sobre os business model canvas, acesse nossa seção do Model Canvas Business](model_canvas_business.md)

## 🔸 Resultados dos experimentos
### Comparação dos modelos rastreados no MLflow:
[Para mais detalhes dos experimentos, acesse a seção de resultados](resultados.md)

##### Comparação das execuções entre modelos:
![Runs comparison](./docs/mlflow_screenshots/2.comparacao_modelos.png)

##### Métricas detalhadas do melhor modelo:
![Best run](./docs/mlflow_screenshots/3.metrics_best_run.png)

## 🔸 Model Card
[Para ter mais detalhes sobre o modelo, acesse nossa seção de Model Card](model_card.md)


## 🔸 Plano de monitoramento
[Para ter mais detalhes sobre o plano de monitoramento do modelo, acesse nossa seção de Plano de Monitoramento](plano_de_monitoramento.md)


## 🙏 Agradecimentos
- Pós Tech Machine Learning - FIAP
- Comunidade open source

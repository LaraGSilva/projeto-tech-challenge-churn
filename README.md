# 📊 Predição de Churn - Telecom

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![MLflow](https://img.shields.io/badge/MLflow-3.3.2-orange.svg)](https://mlflow.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)](https://pytorch.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Projeto de Machine Learning para predição de churn em operadora de telecomunicações usando rede neural MLP (PyTorch) com pipeline completo de MLOps.

## 🎯 Objetivo

Desenvolver um modelo de classificação binária para identificar clientes com alto risco de cancelamento, permitindo intervenções proativas da equipe de CRM e Marketing.

## 📊 Dados

- **Fonte:** [Telco Customer Churn Dataset](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
- **Volume:** 7.043 clientes
- **Target:** Churn (26,5% da base)
- **Formato:** Excel (.xlsx) → Parquet processado

## 🏗️ Arquitetura do Projeto

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

## 🚀 Tecnologias Utilizadas
- **Python 3.8+**
- **PyTorch** - Rede neural MLP
- **Scikit-learn** - Pipelines e métricas
- **MLflow** - Experiment tracking
- **Pandas/Numpy** - Manipulação de dados
- **Matplotlib/Seaborn** - Visualizações
- **Jupyter** - Notebooks interativos

## 📈 Resultados

### Métricas de Performance
- **Recall:** Priorizado para minimizar falsos negativos
- **AUC-ROC:** Discriminação entre classes
- **Accuracy, Precision, F1-Score:** Métricas complementares

### Impacto de Negócio
- **Churn atual:** 26,5% (1.869 clientes)
- **Ticket médio churner:** R$ 74,44/mês
- **Redução estimada:** 20% (450 clientes retidos)

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

## 📋 Funcionalidades

- ✅ **Pipeline completo:** Pré-processamento → Treinamento → Avaliação
- ✅ **Tracking com MLflow:** Experimentos, métricas e artefatos
- ✅ **Modelos baseline:** Comparação com Random Forest, Logistic Regression
- ✅ **Rede Neural MLP:** Implementação em PyTorch
- ✅ **Análise exploratória:** EDA completa com visualizações
- ✅ **Documentação:** Model Canvas com impacto de negócio


## 🙏 Agradecimentos

- Pós Tech Machine Learning - FIAP
- Dataset: [Kaggle - Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
- Comunidade open source
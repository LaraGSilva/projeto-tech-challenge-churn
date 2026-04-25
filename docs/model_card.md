# Tech Challenge - Fase 1 | Model Card 
## Model details

    1. Responsável pelo modelo: Lara Gonçalves;
    2. Data de treinamento do modelo: 25/04/2026;
    3. Versão atual do treinamento: 7;
    4. Tipo de modelo: Modelo de rede neural multicamadas.

## Intended Use
<p>O modelo de rede neural multicamadas foi desenvolvido para <strong>classificar os clientes que são propensos ao churn (cancelamento do produto)</strong>. <br>
O modelo será utilizado pela equipe de CRM da empresa, no qual será responsável pela comunicação e campanhas de retenção para os clientes que estão classificados como possíveis churn na base final.<br>
Este modelo <strong>não</strong> tem a intenção de identificar outros comportamentos do cliente com a empresa a não ser a propensão ao churn, portanto nao deve ser utilizado para prospecção de leads, campanhas de novos produtos ou outros.</p>

## Factors
Fatores relevantes a serem levatandados é que durante os experimentos foram identificados algumas condições que podem influenciar no resultado final como: <br>
    - campo "Churn Reason" e "Churn Value" no dataset: estes campos poderiam afetar o aprendizado do modelo resultando em um overfiting e consequentemente em um aprendizado ruim do modelo.

## Metrics
### Métricas de Desempenho e Impacto
A escolha do modelo final foi guiada pela minimização do Custo Total, priorizando o ROC_AUC para identificar a melhor separação de entre as classes.

    AUC-ROC (Métrica de Separação): 0.847

Indica uma excelente capacidade do modelo em distinguir entre clientes de alto e baixo risco, mantendo a estabilidade em diferentes pontos de corte.

    Custo Total (Métrica de Negócio): R$ 37.635,00

Representa a melhor eficiência financeira entre todos os modelos testados, reduzindo o prejuízo causado por Falsos Negativos (R$ 325/cliente).

    Recall: 92,78%

Alta sensibilidade para garantir que quase a totalidade dos potenciais churns receba uma ação preventiva.

![comparacao_curva_roc_auc](/imgs/curva.png)
### Threshold de Decisão.

    Threshold Aplicado: 0.30

<strong>Justificativa</strong>: O ponto de corte foi otimizado para favorecer o custo financeiro. Dado que um Falso Negativo custa 5x mais que um Falso Positivo, o threshold de 0.30 permite que o modelo seja mais "conservador" em relação à retenção, agindo preventivamente em uma base maior de clientes para garantir a proteção do MRR (Monthly Recurring Revenue).

### Estimativa de Incerteza e Validação
A robustez dos dados reportados é garantida por:

- <strong>Validação em Teste Cego</strong>: As métricas foram extraídas de um conjunto de teste (20% dos dados) totalmente isolado durante o treinamento e ajuste de hiperparâmetros.

- <Strong> Estratificação de Classe </strong>: Utilização de Stratified Shuffle Split para assegurar que a distribuição de churn no teste reflita a realidade do negócio, evitando métricas inflacionadas por amostras não representativas.

- <Strong> Prevenção de Overfitting </strong>: Implementação de Early Stopping e monitoramento de loss em tempo real via MLflow, garantindo que o AUC-ROC reportado seja generalizável para novos dados de produção.

## Evaluation Data
### Datasets utilizados
O modelo foi avaliado utilizando o dataset público **Telco Customer Churn (IBM)** disponível no Kaggle.<br> Este dataset contém aproximadamente <strong>7.043 registros de clientes e 33 variáveis</strong>, incluindo dados demográficos, serviços contratados e informações financeiras, além da variável alvo de churn.

### Motivação da escolha
A escolha desse dataset se deve a:
- Possuir **variáveis relevantes de negócio** (ex: tenure, tipo de contrato, serviços, faturamento), que refletem cenários reais de retenção de clientes.
- Ter um problema bem definido de classificação binária (churn vs. não churn).

### Dados públicos e reprodutibilidade
- O dataset é **público e acessível via Kaggle**, permitindo reprodução dos experimentos.
- Os dados são derivados de um **dataset amostral da IBM**, amplamente documentado e utilizado em estudos acadêmicos e práticos.

### Pré-processamento aplicado
Foi aplicado o seguinte pré-processamento:
- Tratamento de valores nulos (ex: imputação ou remoção)
- Codificação de variáveis categóricas (ex: One-Hot Encoding)
- Padronização/normalização de variáveis numéricas (quando necessário)
- Conversão da variável alvo para formato binário (0/1)
- Separação entre treino e teste

Essas etapas garantem consistência dos dados e evitam vazamento de informação durante a avaliação do modelo.

## Training Data

### Dataset de treino
O modelo foi treinado utilizando o dataset público **Telco Customer Churn (IBM)**, o mesmo utilizado na etapa de avaliação, com divisão entre conjuntos de treino e teste (ex: hold-out ou train/test split).

### Coleta e rotulagem
- Os dados são **sintéticos, porém realistas**, disponibilizados pela IBM e amplamente utilizados para estudos de churn.
- A variável alvo (**Churn**) já está **previamente rotulada** no dataset, indicando se o cliente cancelou o serviço (Yes/No).

### Filtros e amostragem
- Remoção ou tratamento de registros com **valores inconsistentes ou ausentes** (ex: `TotalCharges` vazio).
- Conversão de variáveis categóricas para formato adequado (ex: encoding).
- Separação entre variáveis preditoras e variável alvo.
- Divisão dos dados em treino e teste (ex: 70/30 ou 80/20), garantindo que o conjunto de treino não contenha dados do teste.
- Opcionalmente, pode ter sido aplicado:
  - **Balanceamento de classes** (ex: undersampling/oversampling), devido ao desbalanceamento típico do churn.
  - **Normalização/padronização** de variáveis numéricas.

Esses passos visam garantir qualidade, consistência e representatividade dos dados utilizados no treinamento do modelo.

## Quantitative Analyses
### Visão geral
- **Taxa de churn geral**: 26.54% (1869 de 7043 clientes)
- **Desbalanceamento de classes**: ~73.5% não churn vs ~26.5% churn
- **Ticket médio**:
  - Churn: 73.02
  - Não churn: 61.46  
  → Clientes que churnam possuem, em média, maior receita mensal.

---

### Comportamento por subgrupos

#### Tipo de contrato
- Month-to-month: **42.71%**
- One year: **11.27%**
- Two year: **2.83%**

📌 Forte evidência de que contratos mais longos reduzem churn.

---

#### Internet Service x Phone Service
- Fiber optic + Phone: **41.89%** (maior churn)
- DSL + Phone: **16.62%**
- DSL sem Phone: ~25%
- Sem internet + Phone: **7.40%** (menor churn)

📌 Clientes com fibra apresentam maior risco de churn.

---

#### Geografia (Top cidades)
- San Diego: **33.33%**
- San Francisco: **29.81%**
- Los Angeles: **29.51%**
- San Jose: **25.89%**
- Sacramento: **24.07%**

📌 Variação moderada entre cidades (~24% a ~33%).

---

#### Correlações relevantes
- `tenure` vs churn: **-0.35** → quanto maior o tempo, menor churn  
- `monthly_charges` vs churn: **0.19** → leve associação positiva  
- `churn_score` vs churn: **0.66** → forte relação (esperado)  
- `cltv` vs churn: **-0.13** → leve relação negativa  

---

### Gaps de performance (riscos esperados)
Mesmo sem métricas explícitas por subgrupo, os dados indicam possíveis gaps:

- **Clientes month-to-month** → maior taxa de churn → risco de maior erro (FN/FP)
- **Clientes com fibra** → comportamento distinto → possível viés do modelo
- **Clientes novos (baixo tenure)** → maior churn → podem ser mais difíceis de prever
- **Cidades com maior churn (ex: San Diego)** → potencial variação de performance regional

📌 O modelo pode performar de forma desigual entre esses grupos.

---

### Intervalos de Confiança (IC)
- **Não foram reportados intervalos de confiança (IC)** para as métricas.
- Recomenda-se:
  - Bootstrap para métricas (accuracy, recall, precision)
  - IC por subgrupos críticos (ex: tipo de contrato, tenure)

---

### Conclusão
- O churn é fortemente influenciado por **tipo de contrato, tenure e tipo de serviço**.
- Existe **heterogeneidade entre subgrupos**, indicando risco de viés.
- Avaliações adicionais por segmento são necessárias antes do uso em produção.


## Ethical Considerations
### Uso de dados sensíveis
- O dataset **não contém dados sensíveis diretos**, como informações de saúde, raça ou orientação sexual.
- Inclui apenas dados demográficos básicos (ex: gênero, senioridade), serviços contratados e informações financeiras.

### Riscos de uso indevido
- **Decisões automatizadas injustas**: uso do modelo para negar benefícios ou ofertas pode impactar negativamente certos grupos de clientes.
- **Viés indireto**: variáveis aparentemente neutras (ex: tipo de contrato, tenure) podem atuar como proxies para perfis socioeconômicos.
- **Uso fora de contexto**: aplicar o modelo em populações diferentes da base original pode gerar decisões incorretas.

### Mitigações aplicadas
- **Técnicas**:
  - Monitoramento de métricas por subgrupos (ex: gênero, senioridade), quando possível.
  - Avaliação de métricas além da acurácia (ex: recall, precision), reduzindo impactos assimétricos.
- **Processo**:
  - Uso do modelo como **apoio à decisão**, não como decisão final automatizada.
  - Validação contínua com dados atualizados.
- **Contratuais/organizacionais**:
  - Restrição de uso do modelo apenas para **estratégias de retenção e marketing**, evitando aplicações sensíveis (ex: crédito, elegibilidade).


## Caveats and Recommendations
### Cenários não testados
- O modelo não foi validado em:
  - Outras indústrias ou segmentos fora de telecom.
  - Bases com distribuição de dados significativamente diferente (data drift).
  - Cenários em tempo real (streaming ou decisões online).

### Avaliações adicionais recomendadas
Antes do uso em produção, recomenda-se:
- Testes com **dados reais da empresa** para validar aderência ao contexto.
- Monitoramento de **data drift e concept drift** ao longo do tempo.
- Avaliação de impacto de negócio (ex: custo de falsos positivos vs falsos negativos).
- Testes A/B para medir efetividade em estratégias de retenção.

### Limitações conhecidas
- Dataset relativamente pequeno (~7k registros), podendo limitar generalização.
- Dados **sintéticos/benchmark**, não refletindo completamente a complexidade do mundo real.
- Possível **desbalanceamento da variável alvo (churn)**, impactando métricas.
- O modelo não captura fatores externos relevantes (ex: concorrência, contexto econômico, satisfação do cliente).

Essas limitações devem ser consideradas ao interpretar os resultados e antes da adoção em ambientes produtivos.
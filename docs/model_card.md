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
## Training Data
## Quantitative Analyses
## Ethical Considerations
## Recomendações
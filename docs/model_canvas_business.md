# 📊 Model Canvas: Predição de Churn

## 🎯 Cenário e Objetivo
Operadora de telecom enfrenta churn elevado e precisa identificar clientes com maior risco de abandono rapidamente. Este projeto entrega um pipeline end-to-end com modelo MLP (PyTorch), validação e métricas para priorização de retenção.

![Board de resultados](./imgs/model_canvas_board.png)

## 📉 Diagnóstico e Impacto
- **Volume do problema:** 1.869 churners (26,5% da base).
- **Custo estimado:** R$ 139.000/mês em receita perdida.
- **Insight principal:** clientes churners têm ticket médio de R$ 74,44/mês e prevalecem em contratos mensais (sem fidelidade).

## 👥 Stakeholders e Utilização
- **Usuário Final:** CRM, Marketing de retenção e Produto.
- **Uso:** dashboards de priorização, scores em campanhas segmentadas e automações com alertas em tempo real.

## 📏 Métricas de sucesso
- **Técnica (ML):** Recall alto (priorizar detecção de churn), AUC-ROC (discriminação), Log Loss (calibração).
- **Negócio:** diminuição da taxa de churn e aumento de LTV.

## 📌 Métricas de impacto estimadas
- Redução de churn de 26,5% para 20% = ~450 clientes retidos.
- Valor recuperado potencial: ~R$ 33k/mês (+ ROI de ~24%).

## 📊 Resultados observados
1) **Volume churn:** 1.869 clientes (26,5%).
2) **Perda média por churn:** R$ 74,44/mês (avg_revenue_lost_per_client).

![Distribuição de churn](./imgs/distribuicao_classes_churn.png)

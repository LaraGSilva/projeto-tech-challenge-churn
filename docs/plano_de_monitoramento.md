## 🛰️ Plano de Monitoramento Pós-Implantação

### 1. Monitoramento de Performance do Modelo
O comportamento do cliente de telecomunicações muda rápido. Precisamos garantir que o modelo não "vicie" em dados antigos.

* **Métricas Técnicas:** Monitoramento diário do **AUC-ROC** e **Recall**. Se o Recall cair abaixo de 85%, o modelo está deixando passar muitos churns (aumentando o custo financeiro).
* **Métrica de Negócio (KPI):** Acompanhamento do **Custo Total Real** vs. **Custo Estimado**.
* **Threshold Check:** Validar mensalmente se o threshold de **0.30** ainda é o ponto ótimo de custo-benefício.

### 2. Monitoramento de Dados (Data Drift)
Verifica se as características dos clientes que entram na **FastAPI** são diferentes das usadas no treinamento.

* **Distribuição de Features:** Usar testes estatísticos (como Kolmogorov-Smirnov) para ver se variáveis como `MonthlyCharges` ou `Tenure` mudaram drasticamente.
* **Integridade:** Alertas para valores nulos ou categorias novas (ex: um novo plano de internet) que o modelo não conhece.
* **Volumetria:** Monitorar se a quantidade de predições diárias condiz com o esperado.


### 3. Monitoramento de Infraestrutura (Serving)
Como você está usando **FastAPI** e **SQLite**, o foco é disponibilidade e latência.

* **Latência de Resposta (P99):** Garantir que o endpoint `/predict` responda em menos de 200ms.
* **Taxa de Erro:** Alertas para erros `5XX` (falha no servidor) ou `4XX` (input inválido).
* **Uso de Recursos:** Monitorar consumo de CPU e Memória, especialmente porque Redes Neurais (PyTorch) podem ser mais exigentes que modelos lineares.

---

## 🛠️ Stack Sugerida para Monitoramento

| Componente | Ferramenta | Objetivo |
| :--- | :--- | :--- |
| **Tracking de Experimentos** | **MLflow** | Comparar o modelo de produção com novas versões treinadas. |
| **Métricas de Infra** | **Prometheus + Grafana** | Dashboards em tempo real da saúde da API. |
| **Análise de Drift** | **Evidently AI** | Gerar relatórios de degradação de performance e dados. |
| **Logs de Erro** | **Sentry** | Capturar exceções na FastAPI antes que o usuário reporte. |

---

## 🚨 Gatilhos de Retreinamento (Trigger Policy)
Não se retreina um modelo sem motivo. Estabeleça estas regras:

1.  **Degradação de Performance:** Se o AUC-ROC cair > 5% por 3 dias consecutivos no conjunto de teste diário.
2.  **Drift de Dados:** Se mais de 30% das features principais apresentarem mudança de distribuição estatística.
3.  **Tempo (Scheduled):** Retreinamento preventivo a cada 30 ou 60 dias para incorporar sazonalidades de mercado.

> **Nota Técnica:** Ao retreinar, sempre compare a nova versão com a "MLP Campeã" atual no MLflow. Só substitua em produção se o custo financeiro total for comprovadamente menor na nova versão.
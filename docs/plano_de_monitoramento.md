## 🛰️ Plano de Monitoramento Pós-Implantação

### 1. Monitoramento de Performance do Modelo
O comportamento do cliente de telecomunicações muda rápido. Precisamos garantir que o modelo não "vicie" em dados antigos.
* **Métricas Técnicas:** Monitoramento diário do **AUC-ROC** e **Recall**. Se o Recall cair abaixo de 85%, o modelo está deixando passar muitos churns (aumentando o custo financeiro).
* **Métrica de Negócio (KPI):** Acompanhamento do **Custo Total Real** vs. **Custo Estimado**.
* **Threshold Check:** Validar mensalmente se o threshold de **0.30** ainda é o ponto ótimo de custo-benefício.

### 2. Monitoramento de Dados (Data Drift)
Verificar se as características dos clientes que entram na **FastAPI** são diferentes das usadas no treinamento.
* **Distribuição de Features:** Usar testes estatísticos (como Kolmogorov-Smirnov) para ver se variáveis como `MonthlyCharges` ou `Tenure` mudaram drasticamente.
* **Integridade:** Alertas para valores nulos ou categorias novas (ex: um novo plano de internet) que o modelo não conhece.

### 3. Monitoramento de Infraestrutura (Serving)
* **Latência de Resposta (P99):** Garantir que o endpoint `/predict` responda em menos de 200ms.
* **Taxa de Erro:** Alertas para erros `5XX` (falha no servidor) ou `4XX` (input inválido).
* **Uso de Recursos:** Monitorar consumo de CPU e Memória, especialmente porque Redes Neurais (PyTorch) podem ser mais exigentes que modelos lineares.

---
###  4. Gatilhos de Retreinamento (Trigger Policy)
1.  **Degradação de Performance:** Se o AUC-ROC cair > 5% por 3 dias consecutivos no conjunto de teste diário.
2.  **Drift de Dados:** Se mais de 30% das features principais apresentarem mudança de distribuição estatística.
3.  **Tempo (Scheduled):** Retreinamento preventivo a cada 30 ou 60 dias para incorporar sazonalidades de mercado.

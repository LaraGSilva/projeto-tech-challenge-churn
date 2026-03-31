import mlflow


# Conteúdo: A lógica principal de execução e integração com o MLflow.
# O que deve ter:O bloco with mlflow.start_run().
# Chamadas para mlflow.log_params() e mlflow.log_metrics().
# O comando para salvar o modelo treinado: mlflow.sklearn.log_model().
# Uso de logging estruturado (conforme exigido pelo PDF) em vez de print().


def run_training(X_train, y_train, pipeline, run_name):
    with mlflow.start_run(run_name=run_name):
        pipeline.fit(X_train, y_train)
        # Logs de parâmetros, métricas e o modelo 
        mlflow.sklearn.log_model(pipeline, "model")
        return pipeline
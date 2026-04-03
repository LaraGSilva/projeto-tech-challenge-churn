# Conteúdo: A construção do objeto Pipeline ou ColumnTransformer.O que deve ter:Definição de quais colunas são numéricas e quais são categóricas.
# O OneHotEncoder e o StandardScaler.
# Uma função que recebe os parâmetros do modelo (ex: max_depth do Random Forest) e retorna o pipeline completo pronto para o fit.





from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

def get_rf_pipeline(preprocessador, params):
    """Retorna o pipeline completo com o modelo."""
    return Pipeline([
        ('pre', preprocessador),
        ('model', RandomForestClassifier(**params))
    ])
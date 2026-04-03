import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split

class ChurnPreprocessor:
    def __init__(self):
        self.preprocessor = None
        self.feature_names = None

    def create_pipeline(self,X):
        num_cols = X.select_dtypes(include=['int64','float64']).columns.tolist()
        cat_cols = X.select_dtypes(include=['object']).columns.tolist()

        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(),num_cols),
                ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_cols)
            ]
        )

        return self.preprocessor
    
    def fit_transform(self, X):
        X_transformed = self.preprocessor.fit_transform(X)
        self.feature_names = self.preprocessor.get_feature_names_out()
        return X_transformed
    
    def transform(self, X):
        return self.preprocessor.transform(X)
    
    def save_transformer(Self, path):
        joblib.dump(self.preprocessor,path)

    def load_transformer(self, path):
        self.preprocessor = joblib.load(path)
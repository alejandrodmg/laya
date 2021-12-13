from sklearn.base import BaseEstimator, TransformerMixin
from util.TextProcessing import data_cleaner

class DataCleaner(BaseEstimator, TransformerMixin):
    
    def __init__(self):
        super().__init__()

    def fit(self, X, y=None):
        # Stateless transformer
        return self

    def transform(self, X, y=None):
        # Clean and return data
        X_clean = data_cleaner(X, return_tokens=False)
        return X_clean

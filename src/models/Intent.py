import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

from util.TextProcessing import read_data, X_y_split
from util.CustomTransformers import DataCleaner

class Workflow():

    def __init__(self):
        self.pipeline = Pipeline(
            steps= [
                ('data_cleaner', DataCleaner()),
                ('vectorizer', TfidfVectorizer(ngram_range=(1,1), analyzer='word')),
                ('classifier', RandomForestClassifier(n_estimators=100))
            ])

class IntentClassifier():

    def __init__(self):
        self.model = None
        self.scores = [0, 0]
        self.train(path='../data/intents.txt')

    def update_scores(self, score):
        # Limits lenght of the list to 2
        self.scores.pop(0)
        self.scores.append(score)

    def train(self, path):
        data = read_data(path)
        X, y = X_y_split(data)
        self.model = Workflow()
        self.model.pipeline.fit(X, y)

    def predict(self, X: list):
        scores = self.model.pipeline.predict_proba(X)[0]
        pred = np.argmax(scores)
        self.update_scores(scores[pred])
        return str(pred)

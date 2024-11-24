from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import numpy as np

class PitStopPredictor:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        
    def train(self, data):
        X = data[['volta', 'desgaste_pneus', 'posicao', 'temperatura_pista', 'clima_seco']]
        y = data['pit_stop_realizado']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        return self.model.score(X_test, y_test)
    
    def predict(self, features):
        return self.model.predict_proba(features.reshape(1, -1))[0]
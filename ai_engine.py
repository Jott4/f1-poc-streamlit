import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from transformers import pipeline

class F1StrategyAI:
    def __init__(self):
        self.sequence_model = self._build_sequence_model()
        self.scaler = MinMaxScaler()
        self.sentiment_analyzer = pipeline("sentiment-analysis")
        
    def _build_sequence_model(self):
        model = Sequential([
            LSTM(64, return_sequences=True, input_shape=(10, 5)),
            Dropout(0.2),
            LSTM(32),
            Dense(16, activation='relu'),
            Dense(8, activation='relu'),
            Dense(1, activation='sigmoid')
        ])
        
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        return model
    
    def analyze_race_conditions(self, weather_text):
        """Analisa condições de corrida usando NLP"""
        sentiment = self.sentiment_analyzer(weather_text)
        return sentiment[0]['score']
    
    def predict_tire_degradation(self, historical_data):
        """Prevê degradação dos pneus usando série temporal"""
        scaled_data = self.scaler.fit_transform(historical_data)
        predictions = self.sequence_model.predict(scaled_data)
        return self.scaler.inverse_transform(predictions)
    
    def get_strategy_recommendation(self, current_state):
        """Gera recomendação de estratégia baseada em múltiplos fatores"""
        # Implementação de lógica fuzzy para decisão
        degradation_score = current_state['tire_wear'] * 0.4
        position_score = (20 - current_state['position']) / 20 * 0.3
        weather_score = current_state['weather_condition'] * 0.3
        
        total_score = degradation_score + position_score + weather_score
        
        return {
            'pit_stop_recommended': total_score > 0.6,
            'confidence': total_score,
            'factors': {
                'degradation': degradation_score,
                'position': position_score,
                'weather': weather_score
            }
        }

class RaceDataProcessor:
    def __init__(self):
        self.telemetry_model = self._build_telemetry_model()
        
    def _build_telemetry_model(self):
        model = Sequential([
            Dense(32, activation='relu', input_shape=(10,)),
            Dense(16, activation='relu'),
            Dense(8, activation='relu'),
            Dense(1, activation='linear')
        ])
        model.compile(optimizer='adam', loss='mse')
        return model
    
    def process_telemetry(self, telemetry_data):
        """Processa dados de telemetria em tempo real"""
        processed_data = np.array(telemetry_data).reshape(-1, 10)
        return self.telemetry_model.predict(processed_data)
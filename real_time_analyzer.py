import numpy as np
from datetime import datetime
import pandas as pd

class RealTimeAnalyzer:
    def __init__(self, ai_engine):
        self.ai_engine = ai_engine
        self.historical_data = []
        
    def update_race_status(self, current_data):
        self.historical_data.append(current_data)
        return self._analyze_current_situation()
    
    def _analyze_current_situation(self):
        recent_data = self.historical_data[-10:] if len(self.historical_data) >= 10 else self.historical_data
        
        # Análise de tendências
        trend_analysis = self._analyze_trends(recent_data)
        
        # Previsão de degradação
        degradation_forecast = self._forecast_degradation(recent_data)
        
        return {
            'trend': trend_analysis,
            'forecast': degradation_forecast,
            'recommendation': self._generate_recommendation(trend_analysis, degradation_forecast)
        }
    
    def _analyze_trends(self, data):
        # Implementação de análise de tendências
        if not data:
            return None
            
        df = pd.DataFrame(data)
        trends = {
            'lap_time_trend': df['lap_time'].diff().mean() if 'lap_time' in df else 0,
            'position_trend': df['position'].diff().mean() if 'position' in df else 0,
            'tire_wear_acceleration': df['tire_wear'].diff().diff().mean() if 'tire_wear' in df else 0
        }
        return trends
    
    def _forecast_degradation(self, data):
        if not data:
            return None
            
        # Previsão de degradação para as próximas 5 voltas
        current_state = data[-1]
        forecast = []
        
        for i in range(5):
            next_lap = {
                'lap': current_state['lap'] + i + 1,
                'predicted_wear': current_state['tire_wear'] + (i + 1) * 1.5
            }
            forecast.append(next_lap)
            
        return forecast
    
    def _generate_recommendation(self, trend_analysis, degradation_forecast):
        if not trend_analysis or not degradation_forecast:
            return None
            
        # Lógica de recomendação baseada em múltiplos fatores
        critical_wear = any(lap['predicted_wear'] > 80 for lap in degradation_forecast)
        performance_dropping = trend_analysis['lap_time_trend'] > 0.1
        
        if critical_wear and performance_dropping:
            return "URGENT: Pit stop recommended in next 2 laps"
        elif critical_wear:
            return "WARNING: Plan pit stop within next 5 laps"
        else:
            return "STABLE: Continue current strategy"
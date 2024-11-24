import requests
import pandas as pd
import numpy as np

def get_race_data():
    # Dados simulados para demonstração
    # Em um caso real, você usaria a API Ergast
    data = {
        'volta': list(range(1, 71)),
        'desgaste_pneus': [i * 1.4 for i in range(1, 71)],
        'pit_stop_ideal': [1 if i in [20, 45] else 0 for i in range(1, 71)]
    }
    return pd.DataFrame(data)

def get_historical_pitstops():
    # Dados de exemplo para treinar o modelo
    data = {
        'volta': [],
        'desgaste_pneus': [],
        'posicao': [],
        'temperatura_pista': [],
        'clima_seco': [],
        'pit_stop_realizado': []
    }
    
    # Gerando dados simulados
    for i in range(1000):
        volta = np.random.randint(1, 71)
        desgaste = volta * 1.4 + np.random.normal(0, 5)
        posicao = np.random.randint(1, 21)
        temperatura = np.random.randint(20, 45)
        clima_seco = np.random.choice([0, 1])
        
        # Regra para determinar se o pit stop foi bom
        pit_stop = 1 if (desgaste > 50 and volta > 15) else 0
        
        data['volta'].append(volta)
        data['desgaste_pneus'].append(desgaste)
        data['posicao'].append(posicao)
        data['temperatura_pista'].append(temperatura)
        data['clima_seco'].append(clima_seco)
        data['pit_stop_realizado'].append(pit_stop)
    
    return pd.DataFrame(data)
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from ai_engine import F1StrategyAI, RaceDataProcessor
from real_time_analyzer import RealTimeAnalyzer

# Inicialização dos componentes de IA
@st.cache_resource
def load_ai_components():
    ai_engine = F1StrategyAI()
    race_processor = RaceDataProcessor()
    analyzer = RealTimeAnalyzer(ai_engine)
    return ai_engine, race_processor, analyzer

def create_strategy_visualization(analysis_results):
    fig = go.Figure()
    
    # Adiciona linha de degradação
    x = list(range(len(analysis_results['forecast'])))
    y = [lap['predicted_wear'] for lap in analysis_results['forecast']]
    
    fig.add_trace(go.Scatter(
        x=x, 
        y=y,
        mode='lines+markers',
        name='Predicted Tire Wear'
    ))
    
    # Adiciona zona crítica
    fig.add_hrect(
        y0=80,
        y1=100,
        fillcolor="red",
        opacity=0.2,
        line_width=0,
        name="Critical Zone"
    )
    
    fig.update_layout(
        title='Tire Wear Prediction and Strategy Analysis',
        xaxis_title='Future Laps',
        yaxis_title='Tire Wear (%)',
        height=500
    )
    
    return fig

def main():
    st.title('🏎️ F1 Advanced Strategy AI System')
    
    # Carregando componentes de IA
    ai_engine, race_processor, analyzer = load_ai_components()
    
    # Interface principal
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Current Race Conditions")
        lap = st.number_input('Current Lap', min_value=1, max_value=70, value=10)
        tire_wear = st.slider('Tire Wear (%)', 0, 100, 20)
        position = st.number_input('Current Position', min_value=1, max_value=20, value=5)
        
    with col2:
        st.subheader("Track Conditions")
        temperature = st.slider('Track Temperature (°C)', 20, 45, 30)
        weather = st.selectbox('Weather Conditions', 
                             ['Clear and Dry', 'Light Rain', 'Heavy Rain', 'Mixed Conditions'])
        track_status = st.selectbox('Track Status', 
                                  ['Green', 'Yellow Flag', 'Safety Car', 'Virtual Safety Car'])

    # Processamento em tempo real
    current_data = {
        'lap': lap,
        'tire_wear': tire_wear,
        'position': position,
        'temperature': temperature,
        'weather': weather,
        'track_status': track_status
    }
    
    analysis_results = analyzer.update_race_status(current_data)
    
    # Exibição dos resultados
    st.header('AI Strategy Analysis')
    
    # Métricas principais
    st.metric("Pit Window", f"Optimal: Lap {lap + 5}")
    st.metric("Tire Life", f"{100 - tire_wear}%")
    st.metric("Strategy Confidence", f"{analyzer._analyze_current_situation()['trend']['position_trend']:.2%}")
    
    # Visualização da estratégia
    st.plotly_chart(create_strategy_visualization(analysis_results))
    
    # Recomendações
    st.subheader("Strategy Recommendations")
    recommendation = analysis_results['recommendation']
    
    if "URGENT" in recommendation:
        st.error(recommendation)
    elif "WARNING" in recommendation:
        st.warning(recommendation)
    else:
        st.success(recommendation)
    
    # Análise detalhada
    with st.expander("Detailed Analysis"):
        st.write("Trend Analysis:", analysis_results['trend'])
        st.write("Weather Impact:", ai_engine.analyze_race_conditions(weather))
        
    # Simulação em tempo real
    if st.button('Simulate Next Lap'):
        # Simulação de mudança nas condições
        current_data['lap'] += 1
        current_data['tire_wear'] += np.random.uniform(1, 3)
        new_analysis = analyzer.update_race_status(current_data)
        st.write("Updated Analysis:", new_analysis)

if __name__ == '__main__':
    main()
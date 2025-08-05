import streamlit as st
import plotly.graph_objects as go
from pathlib import Path
import json
from datetime import datetime
import pandas as pd

from utils.feature_extractor import URLFeatureExtractor
from utils.predictor import PhishingPredictor

# Page config
st.set_page_config(
    page_title="Phishing URL Detector",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme and modern UI
st.markdown("""
<style>
    /* Dark theme colors */
    :root {
        --background-color: #0E1117;
        --text-color: #FAFAFA;
        --card-bg: #1E1E1E;
        --success-color: #00CC66;
        --warning-color: #FF4B4B;
    }
    
    /* Main container */
    .main {
        background-color: var(--background-color);
        color: var(--text-color);
    }
    
    /* Cards */
    .stCard {
        background-color: var(--card-bg);
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Custom metric styles */
    .metric-container {
        background-color: var(--card-bg);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.8;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'scan_history' not in st.session_state:
    st.session_state.scan_history = []

def save_scan_result(url, result):
    """Save scan result to history"""
    scan_data = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'url': url,
        'prediction': 'Phishing' if result['prediction'] else 'Legitimate',
        'confidence': f"{result['confidence']*100:.2f}%"
    }
    st.session_state.scan_history.insert(0, scan_data)
    # Keep only last 10 scans
    st.session_state.scan_history = st.session_state.scan_history[:10]

def plot_feature_importance(feature_importance):
    """Create feature importance plot using Plotly"""
    features = []
    shap_values = []
    
    for name, data in feature_importance.items():
        features.append(name)
        shap_values.append(data['shap_value'])
    
    # Create horizontal bar chart
    fig = go.Figure(go.Bar(
        y=features,
        x=shap_values,
        orientation='h',
        marker_color=['#00CC66' if val >= 0 else '#FF4B4B' for val in shap_values]
    ))
    
    fig.update_layout(
        title='Feature Importance (SHAP Values)',
        xaxis_title='Impact on Prediction',
        yaxis_title='Feature',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        showlegend=False
    )
    
    return fig

def main():
    # Header
    st.title("🔒 Phishing URL Detector")
    st.markdown("""
    This application uses machine learning to detect potential phishing URLs.
    Enter a URL below to analyze it for potential security threats.
    """)
    
    # Initialize components
    extractor = URLFeatureExtractor()
    predictor = PhishingPredictor()
    
    # URL input
    url = st.text_input(
        "Enter URL to analyze:",
        placeholder="https://example.com"
    )
    
    if url:
        with st.spinner("Analyzing URL..."):
            try:
                # Extract features
                features = extractor.extract_features(url)
                
                # Get prediction
                result = predictor.predict(features)
                
                # Save to history
                save_scan_result(url, result)
                
                # Display results
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Analysis Results")
                    
                    # Prediction card
                    if result['prediction']:
                        st.error("⚠️ Potential Phishing URL Detected!")
                    else:
                        st.success("✅ Legitimate URL")
                    
                    # Confidence score
                    st.metric(
                        "Confidence Score",
                        f"{result['confidence']*100:.2f}%"
                    )
                
                with col2:
                    st.subheader("Feature Importance")
                    fig = plot_feature_importance(result['feature_importance'])
                    st.plotly_chart(fig, use_container_width=True)
            
            except Exception as e:
                st.error(f"Error analyzing URL: {str(e)}")
    
    # Scan History
    st.sidebar.title("Recent Scans")
    if st.session_state.scan_history:
        history_df = pd.DataFrame(st.session_state.scan_history)
        st.sidebar.dataframe(
            history_df,
            hide_index=True,
            use_container_width=True
        )
    else:
        st.sidebar.info("No scan history yet")

if __name__ == "__main__":
    main() 
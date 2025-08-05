import joblib
import numpy as np
import shap
from pathlib import Path

class PhishingPredictor:
    def __init__(self):
        model_path = Path(__file__).parent.parent / 'model' / 'phishing_model.pkl'
        self.model = joblib.load(model_path)
        self.explainer = shap.TreeExplainer(self.model)
        
        self.feature_names = [
            'URL Length', 'Number of Digits', 'Special Characters',
            'Has IP Address', 'Has @ Symbol', 'Has Double Slash',
            'Domain Length', 'Is Subdomain', 'Domain Age',
            'External Links', 'Has Form', 'Number of iframes'
        ]
    
    def predict(self, features):
        """
        Predict whether a URL is phishing or legitimate
        
        Args:
            features: numpy array of features
            
        Returns:
            dict containing prediction, probability, and SHAP values
        """
        # Reshape features if needed
        if features.ndim == 1:
            features = features.reshape(1, -1)
            
        # Get prediction and probability
        prediction = self.model.predict(features)[0]
        probability = self.model.predict_proba(features)[0]
        
        # Calculate SHAP values
        shap_values = self.explainer.shap_values(features)
        if isinstance(shap_values, list):
            shap_values = shap_values[1]  # For binary classification
            
        # Create feature importance dictionary
        feature_importance = {}
        for idx, name in enumerate(self.feature_names):
            feature_importance[name] = {
                'value': float(features[0][idx]),
                'shap_value': float(shap_values[0][idx])
            }
        
        return {
            'prediction': bool(prediction),
            'confidence': float(max(probability)),
            'feature_importance': feature_importance
        } 
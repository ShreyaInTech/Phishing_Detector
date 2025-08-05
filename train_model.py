import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
from pathlib import Path
import sys

# Add parent directory to path to import utils
sys.path.append(str(Path(__file__).parent.parent))
from utils.feature_extractor import URLFeatureExtractor

def load_and_prepare_data(csv_path):
    """Load and prepare the dataset"""
    df = pd.read_csv(csv_path)
    
    # Extract features for each URL
    extractor = URLFeatureExtractor()
    features = []
    labels = []
    
    print("Extracting features from URLs...")
    for idx, row in df.iterrows():
        if idx % 100 == 0:
            print(f"Processing URL {idx}/{len(df)}")
        
        try:
            url_features = extractor.extract_features(row['url'])
            if -1 not in url_features:  # Only include if all features were extracted
                features.append(url_features)
                labels.append(row['is_phishing'])
        except Exception as e:
            print(f"Error processing URL {row['url']}: {str(e)}")
            continue
    
    return np.array(features), np.array(labels)

def train_model(X, y):
    """Train the Random Forest model"""
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train model
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    print("\nModel Evaluation:")
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))
    
    return model

def main():
    # Setup paths
    current_dir = Path(__file__).parent
    data_path = current_dir.parent / 'data' / 'phishing_dataset.csv'
    model_path = current_dir.parent / 'model' / 'phishing_model.pkl'
    
    # Create model directory if it doesn't exist
    model_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Load and prepare data
    print("Loading dataset...")
    X, y = load_and_prepare_data(data_path)
    
    # Train model
    print("\nTraining model...")
    model = train_model(X, y)
    
    # Save model
    print(f"\nSaving model to {model_path}")
    joblib.dump(model, model_path)
    print("Done!")

if __name__ == "__main__":
    main() 
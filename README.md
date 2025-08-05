# 🔒 Phishing URL Detector

A modern web application built with Streamlit that uses machine learning to detect potential phishing URLs. The application provides real-time analysis of URLs with feature importance visualization using SHAP values.

## Features

- 🔍 Real-time URL analysis
- 📊 Feature importance visualization using SHAP values
- 📱 Responsive dark theme UI
- 📜 Recent scan history
- 🤖 Machine learning-based detection
- 🔄 Comprehensive feature extraction

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/phishing_detector_streamlit.git
cd phishing_detector_streamlit
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. First, train the model:
```bash
python training/train_model.py
```

2. Run the Streamlit app:
```bash
streamlit run app.py
```

3. Open your browser and navigate to the URL shown in the terminal (usually http://localhost:8501)

## Project Structure

```
phishing_detector_streamlit/
│
├── app.py                      # Main Streamlit app
├── model/
│   └── phishing_model.pkl      # Trained ML model
│
├── utils/
│   ├── feature_extractor.py    # URL feature extraction
│   └── predictor.py            # Model prediction
│
├── training/
│   └── train_model.py          # Model training script
│
├── data/
│   └── phishing_dataset.csv    # Training dataset
│
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Features Extracted

The application extracts the following features from URLs:
- URL length
- Number of digits
- Special characters count
- IP address presence
- @ symbol presence
- Double slash presence
- Domain length
- Subdomain presence
- Domain age
- External links count
- Form presence
- Number of iframes

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
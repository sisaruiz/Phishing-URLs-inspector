# Phishing URL Detector

This is a web-based application that detects phishing URLs using a machine learning model trained on URL-based features.

## Application Usage

Users can input a URL through the web interface. The application extracts relevant features from the URL, passes them to the trained model, and outputs a prediction indicating whether the URL is likely to be safe or phishing.

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/your-username/phishing-url-detector.git
cd phishing-url-detector
```

2. **Set up a virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

## Model Training

Before running the application, you must generate and save the trained machine learning model.

To do this:

- Open and run the notebooks located in the `data mining and machine learning` folder.
- These notebooks handle feature extraction, data preprocessing, model training, and saving the trained model.

Make sure the final trained model is saved in `model\random_forest_model.pkl`.

## Running the Application

After generating the trained model, you can start the web application with:

```bash
python app.py
```

Then, open your browser and navigate to:

```
http://localhost:5000
```

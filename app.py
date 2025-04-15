from flask import Flask, render_template, request
import joblib
import os
from utils.feature_extraction import extract_features

app = Flask(__name__)

# Load model
model = joblib.load(os.path.join("model", "rf_model.joblib"))

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction = None
    if request.method == 'POST':
        url = request.form['url']
        features = extract_features(url)  # Feature extraction pipeline
        prediction = model.predict([features])[0]
    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)

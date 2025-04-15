from flask import Flask, render_template, request
import joblib
import os
import pandas as pd
from utils.feature_extraction import extract_features

app = Flask(__name__)

# Load model
model = joblib.load(os.path.join("model", "rf_model.joblib"))

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction = None
    probability = None  # Initialize the probability variable
    if request.method == 'POST':
        url = request.form['url']
        
        # Extract features from the URL
        features = extract_features(url)

        # Ensure features match the training data's column order
        X = pd.DataFrame([features])
        training_columns = [  # Same order used during training
            'shannon_entropy', 'directory_length', 'has_dir', 'file_length', 'length_url',
            'qty_dot_params', 'qty_dot_url', 'qty_hyphen_directory', 'qty_underline_params',
            'qty_slash_params', 'qty_slash_url', 'domain_length', 'qty_at_params',
            'qty_hyphen_params', 'qty_hashtag_params', 'qty_comma_params',
            'qty_exclamation_params', 'qty_vowels_domain', 'qty_hyphen_file',
            'qty_asterisk_params', 'qty_dollar_params', 'has_file',
            'qty_questionmark_params', 'qty_tilde_params', 'qty_dot_domain',
            'params_length', 'qty_slash_directory', 'qty_and_params', 'qty_equal_params',
            'qty_plus_params', 'qty_dot_directory', 'qty_underline_file',
            'qty_percent_params', 'qty_hyphen_domain', 'qty_hyphen_url'
        ]
        X = X[training_columns]

        # Get the prediction and probability for the "bad" class
        prob = model.predict_proba(X)
        prediction = model.predict(X)[0]  # Predicted class (0 or 1)
        probability = prob[0][1]  # Probability of being "bad" (malicious)

    return render_template('index.html', prediction=prediction, probability=probability)

if __name__ == '__main__':
    app.run(debug=True)
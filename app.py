from flask import Flask, render_template, request
import joblib
import os
import pandas as pd
from utils.feature_extraction import extract_features

app = Flask(__name__)

model = joblib.load(os.path.join("model", "random_forest_model.pkl"))

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction = None
    probability = None 
    if request.method == 'POST':
        url = request.form['url']
        
        features = extract_features(url)

        X = pd.DataFrame([features])
        training_columns = [  # order used during training
            'qty_dot_url', 'qty_hyphen_url', 'qty_slash_url', 'qty_questionmark_url', 'qty_equal_url',
            'qty_and_url', 'qty_plus_url', 'qty_tld_url', 'length_url', 'qty_dot_domain', 'qty_hyphen_domain',
            'qty_vowels_domain', 'domain_length', 'has_dir', 'qty_dot_directory', 'qty_hyphen_directory',
            'qty_underline_directory', 'qty_slash_directory', 'qty_plus_directory', 'directory_length',
            'has_file', 'qty_dot_file', 'qty_hyphen_file', 'qty_underline_file', 'file_length', 'has_params',
            'qty_dot_params', 'qty_slash_params', 'qty_questionmark_params', 'qty_equal_params', 'qty_and_params',
            'params_length', 'tld_present_params', 'qty_params', 'shannon_entropy'
        ]
        X = X[training_columns]

        prob = model.predict_proba(X)
        prediction = model.predict(X)[0]  # predicted class (0 or 1)
        probability = prob[0][1]  # probability of being "bad"

    return render_template('index.html', prediction=prediction, probability=probability)

if __name__ == '__main__':
    app.run(debug=True)
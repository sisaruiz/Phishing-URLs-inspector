import re
import numpy as np
from urllib.parse import urlparse

# Function to calculate Shannon entropy
def shannon_entropy(url):
    if not url:
        return 0
    prob = [url.count(c) / len(url) for c in set(url)]
    return -sum(p * np.log2(p) for p in prob)

# Function to extract features from the URL
def extract_url_features(url):
    features = {}
    features['qty_dot_url'] = url.count('.')
    features['qty_hyphen_url'] = url.count('-')
    features['qty_slash_url'] = url.count('/')
    features['length_url'] = len(url)
    return features

# Function to extract domain from URL
def extract_domain(url):
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    domain = re.findall(r'://(.*?)(/|$)', url)
    if domain:
        return domain[0][0]
    else:
        if url.startswith('www.'):
            return url.split('/')[0].replace('www.', '')
        return url.split('/')[0]

# Function to extract domain features
def extract_domain_features(domain):
    features = {}
    features['qty_dot_domain'] = domain.count('.')
    features['qty_hyphen_domain'] = domain.count('-')
    features['qty_vowels_domain'] = sum([1 for char in domain if char.lower() in 'aeiou'])
    features['domain_length'] = len(domain)
    return features

# Function to extract directory from URL
def extract_directory(url):
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    match = re.search(r'://[^/]+(/.*?)(\?|$)', url)
    if match:
        return match.group(1)
    return None

# Function to extract directory-related features
def extract_directory_features(directory):
    features = {}
    if directory is None:
        features['has_dir'] = 0
        features['qty_hyphen_directory'] = -1
        features['qty_slash_directory'] = -1
        features['qty_dot_directory'] = -1
        features['directory_length'] = 0
    else:
        features['has_dir'] = 1
        features['qty_hyphen_directory'] = directory.count('-')
        features['qty_slash_directory'] = directory.count('/')
        features['qty_dot_directory'] = directory.count('.')
        features['directory_length'] = len(directory)
    return features

# Function to extract file from URL
def extract_file(url):
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    match = re.search(r'\/([^\/\?]*)(\?|$)', url)
    if match:
        return match.group(1) if match.group(1) else None
    return None

# Function to extract file-related features
def extract_file_features(file):
    features = {}
    if file is None or file == '':
        features['has_file'] = 0
        features['qty_hyphen_file'] = -1
        features['file_length'] = 0
        features['qty_underline_file'] = -1
    else:
        features['has_file'] = 1
        features['qty_hyphen_file'] = file.count('-')
        features['file_length'] = len(file)
        features['qty_underline_file'] = file.count('_')
    return features

# Function to extract parameters from URL
def extract_params(url):
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    match = re.search(r'\?(.*)', url)
    if match:
        return match.group(1)
    return None

# Function to extract parameters-related features
def extract_params_features(params):
    features = {}
    if params is None:
        features = {key: -1 for key in [
            'qty_dot_params', 'qty_slash_params', 'qty_comma_params', 'qty_at_params',
            'qty_hyphen_params', 'qty_dollar_params', 'qty_asterisk_params', 'qty_underline_params',
            'qty_questionmark_params', 'qty_equal_params', 'qty_and_params', 'qty_exclamation_params',
            'qty_tilde_params', 'qty_plus_params', 'qty_hashtag_params', 'qty_percent_params'
        ]}
        features['params_length'] = 0
    else:
        features['qty_dot_params'] = params.count('.')
        features['qty_slash_params'] = params.count('/')
        features['qty_comma_params'] = params.count(',')
        features['qty_at_params'] = params.count('@')
        features['qty_hyphen_params'] = params.count('-')
        features['qty_dollar_params'] = params.count('$')
        features['qty_asterisk_params'] = params.count('*')
        features['qty_underline_params'] = params.count('_')
        features['qty_questionmark_params'] = params.count('?')
        features['qty_equal_params'] = params.count('=')
        features['qty_and_params'] = params.count('&')
        features['qty_exclamation_params'] = params.count('!')
        features['qty_tilde_params'] = params.count('~')
        features['qty_plus_params'] = params.count('+')
        features['qty_hashtag_params'] = params.count('#')
        features['qty_percent_params'] = params.count('%')
        features['params_length'] = len(params)
    return features

# Master function that combines all features extraction
def extract_features(url):
    url_features = extract_url_features(url)
    domain = extract_domain(url)
    domain_features = extract_domain_features(domain)
    directory = extract_directory(url)
    directory_features = extract_directory_features(directory)
    file = extract_file(url)
    file_features = extract_file_features(file)
    params = extract_params(url)
    params_features = extract_params_features(params)
    
    all_features = {**url_features, **domain_features, **directory_features, **file_features, **params_features}
    all_features['shannon_entropy'] = shannon_entropy(url)
    
    return all_features
import re
import numpy as np
from urllib.parse import urlparse, parse_qs

# Function to calculate Shannon entropy
def shannon_entropy(url):
    if not url:
        return 0
    prob = [url.count(c) / len(url) for c in set(url)]
    return -sum(p * np.log2(p) for p in prob)

# URL-level features
def extract_url_features(url):
    features = {}
    features['qty_dot_url'] = url.count('.')
    features['qty_hyphen_url'] = url.count('-')
    features['qty_slash_url'] = url.count('/')
    features['qty_questionmark_url'] = url.count('?')
    features['qty_equal_url'] = url.count('=')
    features['qty_and_url'] = url.count('&')
    features['qty_plus_url'] = url.count('+')
    tld_pattern = r'\.[a-z]{2,}$'
    features['qty_tld_url'] = len(re.findall(tld_pattern, url))
    features['length_url'] = len(url)
    return features

# Extract domain from URL
def extract_domain(url):
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    parsed = urlparse(url)
    return parsed.netloc

# Domain-level features
def extract_domain_features(domain):
    features = {}
    features['qty_dot_domain'] = domain.count('.')
    features['qty_hyphen_domain'] = domain.count('-')
    features['qty_vowels_domain'] = sum([1 for char in domain if char.lower() in 'aeiou'])
    features['domain_length'] = len(domain)
    return features

# Extract directory from URL
def extract_directory(url):
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    parsed = urlparse(url)
    return parsed.path if parsed.path else None

# Directory-level features
def extract_directory_features(directory):
    features = {}
    if not directory:
        features['has_dir'] = 0
        features['qty_dot_directory'] = 0
        features['qty_hyphen_directory'] = 0
        features['qty_underline_directory'] = 0
        features['qty_slash_directory'] = 0
        features['qty_plus_directory'] = 0
        features['directory_length'] = 0
    else:
        features['has_dir'] = 1
        features['qty_dot_directory'] = directory.count('.')
        features['qty_hyphen_directory'] = directory.count('-')
        features['qty_underline_directory'] = directory.count('_')
        features['qty_slash_directory'] = directory.count('/')
        features['qty_plus_directory'] = directory.count('+')
        features['directory_length'] = len(directory)
    return features

# Extract file from URL
def extract_file(url):
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    parsed = urlparse(url)
    path = parsed.path
    if '/' in path:
        file = path.split('/')[-1]
        return file if file else None
    return None

# File-level features
def extract_file_features(file):
    features = {}
    if not file:
        features['has_file'] = 0
        features['qty_dot_file'] = 0
        features['qty_hyphen_file'] = 0
        features['qty_underline_file'] = 0
        features['file_length'] = 0
    else:
        features['has_file'] = 1
        features['qty_dot_file'] = file.count('.')
        features['qty_hyphen_file'] = file.count('-')
        features['qty_underline_file'] = file.count('_')
        features['file_length'] = len(file)
    return features

# Extract parameters from URL
def extract_params(url):
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    parsed = urlparse(url)
    return parsed.query if parsed.query else None

# Parameters-level features
def extract_params_features(params):
    features = {}
    if not params:
        features['has_params'] = 0
        features['qty_dot_params'] = 0
        features['qty_slash_params'] = 0
        features['qty_questionmark_params'] = 0
        features['qty_equal_params'] = 0
        features['qty_and_params'] = 0
        features['params_length'] = 0
        features['tld_present_params'] = 0
        features['qty_params'] = 0
    else:
        features['has_params'] = 1
        features['qty_dot_params'] = params.count('.')
        features['qty_slash_params'] = params.count('/')
        features['qty_questionmark_params'] = params.count('?')
        features['qty_equal_params'] = params.count('=')
        features['qty_and_params'] = params.count('&')
        features['params_length'] = len(params)
        features['tld_present_params'] = int(bool(re.search(r'\.[a-z]{2,}', params)))
        features['qty_params'] = len(parse_qs(params))
    return features

# Master function that combines everything
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

    all_features = {
        **url_features,
        **domain_features,
        **directory_features,
        **file_features,
        **params_features,
        'shannon_entropy': shannon_entropy(url)
    }
    return all_features

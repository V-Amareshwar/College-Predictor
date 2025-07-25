import yaml
import joblib
import os

def load_config(config_path):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def save_model(model, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(model, path)
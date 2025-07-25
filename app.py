from flask import Flask
from flask_cors import CORS
from routes import init_routes
import pandas as pd
import joblib
from src.utils import load_config
import os

def create_app():
    app = Flask(__name__, template_folder="../frontend/templates", static_folder="../frontend/static")
    CORS(app)

    # Load config
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    config_path = os.path.join(project_root, 'config', 'config.yaml')
    config = load_config(config_path)

    # Adjust paths
    config['model']['path'] = os.path.join(project_root, config['model']['path'])
    config['model']['features_path'] = os.path.join(project_root, config['model']['features_path'])
    config['data']['combined_data'] = os.path.join(project_root, config['data']['combined_data'])
    config['outputs']['predictions_dir'] = os.path.join(project_root, config['outputs']['predictions_dir'])

    # Preload model and 2024 data
    app.model = joblib.load(config['model']['path'])
    app.df_2024 = pd.read_csv(config['data']['combined_data'])
    app.df_2024 = app.df_2024[app.df_2024['year'] == 2024]
    app.feature_cols = joblib.load(config['model']['features_path'])['feature_cols']
    app.config_data = config

    init_routes(app)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
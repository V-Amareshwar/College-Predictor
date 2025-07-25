import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import render_template, request, jsonify
from src.predict import predict_colleges

def init_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/api/predict', methods=['POST'])
    def predict():
        try:
            data = request.get_json()
            rank = data.get('rank')
            category = data.get('category')
            gender = data.get('gender')
            preferred_branches = data.get('preferred_branches')
            num_predictions = data.get('num_predictions', 10)

            # Input validation
            if not all([rank, category, gender]):
                return jsonify({'error': 'Missing required fields'}), 400
            if not isinstance(rank, int) or rank < 1:
                return jsonify({'error': 'Invalid rank'}), 400
            if category not in ['OC', 'BC-A', 'BC-B', 'BC-C', 'BC-D', 'BC-E', 'SC', 'ST']:
                return jsonify({'error': 'Invalid category'}), 400
            if gender not in ['Boy', 'Girl']:
                return jsonify({'error': 'Invalid gender'}), 400
            if preferred_branches and not isinstance(preferred_branches, list):
                return jsonify({'error': 'Preferred branches must be a list'}), 400

            # Use preloaded model and data
            predictions_df = predict_colleges(
                app.config_data,
                rank,
                category,
                gender,
                preferred_branches,
                model=app.model,
                df_2024=app.df_2024,
                feature_cols=app.feature_cols
            )

            if predictions_df.empty:
                return jsonify({'predictions': []})

            predictions = predictions_df.to_dict(orient='records')
            formatted_predictions = [
                {
                    'college_name': pred['college_name'],
                    'branch': pred['branch'],
                    'predicted_closing_rank': pred['predicted_closing_rank'],
                    'college_prestige': pred['college_prestige']
                } for pred in predictions
            ]

            return jsonify({'predictions': formatted_predictions})
        except Exception as e:
            return jsonify({'error': f'Prediction failed: {str(e)}'}), 500
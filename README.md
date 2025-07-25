Telangana EAPCET College Prediction
This project predicts eligible colleges for Telangana EAPCET based on historical cutoff data (2019–2022, 2024).
Folder Structure

data/: Raw and processed data.
raw/: Contains 2019.xlsx, 2020.xlsx, etc.
processed/: Contains combined_data.csv and branch_mapping.csv.


src/: Python scripts for preprocessing, training, and prediction.
models/: Trained model files.
notebooks/: EDA notebooks.
outputs/: Predictions and visualizations.
config/: Configuration files.

Setup

Install dependencies:pip install -r requirements.txt


Place raw Excel files (2019.xlsx, 2020.xlsx, 2021.xlsx, 2022.xlsx, 2024.xlsx) in data/raw/.
Update config/config.yaml with correct paths if needed.
Update predict.py with correct mappings for category, gender, and branch_id.

Usage
Run the pipeline:
python main.py

Follow the prompts to enter your rank, category, gender, and preferred branches.
Model

Type: Random Forest Regressor
Features: Year, college_id, branch_id, category, gender
Target: Closing rank

Outputs

Trained model: models/random_forest_model.pkl
Branch mapping: data/processed/branch_mapping.csv
Predictions: outputs/predictions/sample_predictions.csv
Feature importance plot: outputs/figures/feature_importance.png


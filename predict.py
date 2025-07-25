import pandas as pd
import numpy as np

def predict_colleges(config, rank, category, gender, preferred_branches=None, model=None, df_2024=None, feature_cols=None):
    try:
        if model is None or df_2024 is None or feature_cols is None:
            raise ValueError("Model, data, or feature columns not provided")

        df = df_2024.copy()

        # Feature engineering
        college_avg_rank = df.groupby('college_id')['closing_rank'].mean()
        college_prestige = 1 / college_avg_rank
        college_prestige = (college_prestige - college_prestige.min()) / (college_prestige.max() - college_prestige.min())
        df['college_prestige'] = df['college_id'].map(college_prestige)
        
        branch_popularity = df.groupby('branch_id').size()
        branch_popularity = (branch_popularity - branch_popularity.min()) / (branch_popularity.max() - branch_popularity.min())
        df['branch_popularity'] = df['branch_id'].map(branch_popularity)
        
        df['rank_stability'] = df.groupby(['college_id', 'branch_id'])['closing_rank'].transform('std').fillna(0)
        df['avg_closing_rank'] = df.groupby(['college_id', 'branch_id'])['closing_rank'].transform('mean')
        
        college_branch_avg_rank = df.groupby(['college_id', 'branch_id'])['closing_rank'].mean()
        college_branch_prestige = 1 / college_branch_avg_rank
        college_branch_prestige = (college_branch_prestige - college_branch_prestige.min()) / (college_branch_prestige.max() - college_branch_prestige.min())
        df['college_branch_prestige'] = df[['college_id', 'branch_id']].apply(
            lambda x: college_branch_prestige.get((x['college_id'], x['branch_id']), 0.5), axis=1
        )
        
        df['log_rank'] = np.log1p(df['closing_rank'])
        
        college_target = df.groupby('college_id')['closing_rank'].mean()
        df['college_id_encoded'] = df['college_id'].map(college_target)
        branch_target = df.groupby('branch_id')['closing_rank'].mean()
        df['branch_id_encoded'] = df['branch_id'].map(branch_target)
        
        categorical_cols = ['category', 'gender']
        df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
        
        for col in feature_cols:
            if col not in df_encoded.columns:
                df_encoded[col] = 0
        
        predictions = []
        seen = set()
        rank_threshold = rank + 2000 if rank <= 10000 else rank + 4000
        for idx, row in df.iterrows():
            if preferred_branches and row['branch_id'] not in preferred_branches:
                continue
            input_data = df_encoded.loc[[idx], feature_cols]
            pred_rank = model.predict(input_data)[0]
            if rank <= pred_rank <= rank_threshold:
                key = (row['college_name'], row['branch_id'])
                if key not in seen:
                    seen.add(key)
                    predictions.append({
                        'college_name': row['college_name'],
                        'branch': row['branch_id'],
                        'predicted_closing_rank': pred_rank,
                        'college_prestige': row['college_prestige']
                    })
        
        predictions_df = pd.DataFrame(predictions)
        if not predictions_df.empty:
            predictions_df = predictions_df.sort_values('predicted_closing_rank').head(10)
        
        return predictions_df
    except Exception as e:
        raise
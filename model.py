"""
Soccer Prediction Bot
Author: Talk2Mayor
Date: January 19, 2024
Description: This Python script predicts soccer match outcomes using machine learning.
"""


from sklearn.preprocessing import LabelEncoder

def encode_teams(label_encoder, df):
    df['home_team'] = label_encoder.fit_transform(df['home_team'])
    df['away_team'] = label_encoder.transform(df['away_team'])
    return df

def make_predictions(classifier, label_encoder, home_team, away_team, year):
    prediction_data = pd.DataFrame({'home_team': [label_encoder.transform([home_team])[0]], 'away_team': [label_encoder.transform([away_team])[0]], 'year': [year]})
    outcome_prediction = classifier.predict(prediction_data)

    return outcome_prediction

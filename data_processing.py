"""
Soccer Prediction Bot
Author: Talk2Mayor
Date: January 19, 2024
Description: This Python script predicts soccer match outcomes using machine learning.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import requests
from datetime import datetime

def preprocess_data(df):
     # Handle missing values if any
    df = df.dropna()

    # Encode categorical variables using LabelEncoder
    label_encoder = LabelEncoder()
    df['home_team'] = label_encoder.fit_transform(df['home_team'])
    df['away_team'] = label_encoder.transform(df['away_team'])

    # Optionally, you can perform additional feature engineering or scaling here
    # Example: Create a new feature for the goal difference
    #df['goal_difference'] = df['home_team_goal'] - df['away_team_goal']

    return df
def split_data(df):
    features = df[['home_team', 'away_team', 'year']]
    target = df['outcome']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test

def train_classifier(X_train, y_train):
    classifier = RandomForestClassifier(n_estimators=100, random_state=42)
    classifier.fit(X_train, y_train)
    return classifier

def update_and_save_data(api_key, competition_code, historical_data_file):
    live_matches = get_live_matches(api_key, competition_code)

    if live_matches:
        # Load existing historical data
        try:
            historical_data = pd.read_csv(historical_data_file)
        except FileNotFoundError:
            historical_data = pd.DataFrame(columns=['home_team', 'away_team', 'year', 'outcome'])

        # Preprocess the live match data
        new_data = []
        for match in live_matches:
            home_team = match["homeTeam"]["name"]
            away_team = match["awayTeam"]["name"]
            year = datetime.now().year

            # You can use a simple heuristic for the outcome prediction based on real-time data
            outcome = 1 if match["score"]["fullTime"]["homeTeam"] > match["score"]["fullTime"]["awayTeam"] else (
                -1 if match["score"]["fullTime"]["homeTeam"] < match["score"]["fullTime"]["awayTeam"] else 0)

            new_data.append({'home_team': home_team, 'away_team': away_team, 'year': year, 'outcome': outcome})

        # Append new data to the historical dataset
        historical_data = historical_data.append(new_data, ignore_index=True)

        # Save the updated dataset
        historical_data.to_csv(historical_data_file, index=False)
def create_or_load_historical_data(historical_data_file):
    try:
        return pd.read_csv(historical_data_file)
    except FileNotFoundError:
        return pd.DataFrame(columns=['home_team', 'away_team', 'year', 'outcome'])

def get_live_matches(api_key, competition_code):
    base_url = f"https://api.football-data.org/v2/matches"
    headers = {"X-Auth-Token": api_key}
    params = {"competitions": competition_code, "status": "LIVE"}

    response = requests.get(base_url, headers=headers, params=params)
    data = response.json()

    if response.status_code == 200:
        return data.get("matches", [])
    else:
        print(f"Error fetching live match data: {response.status_code}")
        return None

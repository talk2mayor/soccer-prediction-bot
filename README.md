# Soccer Prediction Bot

## Overview

The Soccer Prediction App is a Python application that predicts the outcomes of soccer matches using machine learning. It integrates with a soccer data API to fetch live and historical match data, processes the data, and makes predictions for upcoming matches.

## Features

- **Live Predictions:** Get real-time predictions for live soccer matches.
- **Historical Data:** Use historical match data for training and improving prediction accuracy.
- **User Interface:** A simple and interactive UI for selecting match types, entering years, and viewing predictions.

## Prerequisites

Before running the app, ensure you have the following dependencies installed:

- Python 3.x
- PyQt5
- scikit-learn
- requests

## Getting Started
 Clone the repository:
- git clone https://github.com/talk2mayor/soccer-prediction-bot.git
- cd soccer-prediction-bot

## Replace YOUR_API_KEY in ui.py and fixtures.py with your actual API key from Football Data API.

## Run the app:
python ui.py


## Application Structure
- ui.py: Main module for the Soccer Prediction App UI.
- data_processing.py: Module for data preprocessing and training.
- model.py: Module for encoding teams and making predictions.
- fixtures.py: Module for displaying upcoming and played fixtures.


## Usage
- Launch the app using python ui.py.
- Select the match type, enter the year, and click "Predict."
- View the predictions for live matches and historical results.

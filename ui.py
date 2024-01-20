"""
Soccer Prediction Bot
Author: Talk2Mayor
Date: January 19, 2024
Description: This Python script predicts soccer match outcomes using machine learning.
"""


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTextEdit, QProgressBar, QMessageBox
from PyQt5.QtCore import Qt, QEvent
from datetime import datetime
from data_processing import preprocess_data, split_data, train_classifier, create_or_load_historical_data, get_live_matches
from model import encode_teams, make_predictions
from sklearn.preprocessing import LabelEncoder
from PyQt5.QtWidgets import QToolTip


class SoccerPredictionApp(QWidget):
    def __init__(self, api_key):
        super().__init__()
        self.api_key = api_key
        self.init_ui()

    def init_ui(self):
        # UI Elements
        self.match_type_label = QLabel('Select Match Type:')
        self.match_type_combobox = QLineEdit()
        self.match_type_combobox.setPlaceholderText("e.g., Premier League")
        self.match_type_combobox.installEventFilter(self)

        self.year_label = QLabel('Enter Year:')
        self.year_entry = QLineEdit()
        self.year_entry.setPlaceholderText("e.g., 2023")
        self.year_entry.installEventFilter(self)

        self.predict_button = QPushButton('Predict')
        self.predict_button.clicked.connect(self.predict_button_click)

        self.predictions_text = QTextEdit()
        self.predictions_text.setReadOnly(True)

        self.progress_bar = QProgressBar()
        self.status_label = QLabel('Status: Ready')

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.match_type_label)
        layout.addWidget(self.match_type_combobox)
        layout.addWidget(self.year_label)
        layout.addWidget(self.year_entry)
        layout.addWidget(self.predict_button)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.predictions_text)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

        # Set up the main window
        self.setGeometry(100, 100, 400, 400)
        self.setWindowTitle('Soccer Prediction App')

    def eventFilter(self, obj, event):
        if event.type() == QEvent.FocusIn:
            if obj == self.match_type_combobox:
                QToolTip.showText(self.mapToGlobal(obj.pos()), "Enter the match type (e.g., Premier League)")
            elif obj == self.year_entry:
                QToolTip.showText(self.mapToGlobal(obj.pos()), "Enter the year (e.g., 2023)")
        return super().eventFilter(obj, event)

    def predict_button_click(self):
        selected_match_type = self.match_type_combobox.text().strip()
        selected_year = self.year_entry.text().strip()

        if not selected_match_type or not selected_year:
            QMessageBox.critical(self, 'Error', 'Please enter valid match type and year.')
            return

        try:
            selected_year = int(selected_year)
        except ValueError:
            QMessageBox.critical(self, 'Error', 'Invalid year. Please enter a valid numerical year.')
            return

        live_matches = get_live_matches(self.api_key, selected_match_type)

        if live_matches:
            # Load or create historical data
            historical_data_file = 'historical_data.csv'  # Replace with your actual file path
            historical_data = create_or_load_historical_data(historical_data_file)

            # Preprocess the historical data
            features = preprocess_data(historical_data)
            X_train, X_test, y_train, y_test = split_data(features)

            # Train a Random Forest classifier
            classifier = train_classifier(X_train, y_train)

            # Display predictions for live matches
            self.predictions_text.clear()
            self.progress_bar.setValue(0)
            self.status_label.setText('Status: Predicting...')

            label_encoder = LabelEncoder()
            features = encode_teams(label_encoder, historical_data)

            total_matches = len(live_matches)
            matches_processed = 0

            for match in live_matches:
                home_team = match["homeTeam"]["name"]
                away_team = match["awayTeam"]["name"]
                year = datetime.now().year

                # Make predictions
                outcome_prediction = make_predictions(classifier, label_encoder, home_team, away_team, year)

                # Interpret the prediction
                prediction_text = f"Prediction for {home_team} vs {away_team}: "
                if outcome_prediction[0] == 1:
                    prediction_text += "Home team wins!\n"
                elif outcome_prediction[0] == -1:
                    prediction_text += "Away team wins!\n"
                else:
                    prediction_text += "It's a draw!\n"

                self.predictions_text.append(prediction_text)

                # Update progress bar and status label
                matches_processed += 1
                progress_value = int((matches_processed / total_matches) * 100)
                self.progress_bar.setValue(progress_value)
                self.status_label.setText(f'Status: {matches_processed}/{total_matches} matches processed')

            self.status_label.setText('Status: Prediction completed')

if __name__ == '__main__':
    api_key = "YOUR API"  # Replace with your actual API key
    app = QApplication(sys.argv)
    main_window = SoccerPredictionApp(api_key)
    main_window.show()
    sys.exit(app.exec_())

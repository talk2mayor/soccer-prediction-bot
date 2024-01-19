import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QTextEdit, QCheckBox, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt
import requests

class FixtureDisplayApp(QWidget):
    def __init__(self, api_key):
        super().__init__()
        self.api_key = api_key
        self.init_ui()

    def checkbox_clicked(self, state, match_checkbox, match):
        if state == Qt.Checked:
            self.selected_matches.append(match)
        else:
            self.selected_matches.remove(match)
    def checkbox_clicked(self, state, checkbox, match):
        if state == Qt.Checked:
            mouse_event = QMouseEvent(QEvent.MouseButtonDblClick, QPointF(), Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
            self.show_match_details(checkbox, match, mouse_event)


    def print_selected_matches(self):
        if not self.selected_matches:
            QMessageBox.information(self, "Print Selected Matches", "No matches selected.", QMessageBox.Ok)
            return

        print("Selected Matches:")
        for match in self.selected_matches:
            print(f"Home Team: {match['homeTeam']['name']}, Away Team: {match['awayTeam']['name']}, Date: {match['utcDate']}")

    def export_selected_matches(self):
        if not self.selected_matches:
            QMessageBox.information(self, "Export Selected Matches", "No matches selected.", QMessageBox.Ok)
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Export Selected Matches", "", "Text Files (*.txt);;All Files (*)")

        if file_path:
            with open(file_path, 'w') as file:
                file.write("Selected Matches:\n")
                for match in self.selected_matches:
                    file.write(f"Home Team: {match['homeTeam']['name']}, Away Team: {match['awayTeam']['name']}, Date: {match['utcDate']}\n")

    def show_match_details(self, match):
        # Display match details in a QMessageBox
        details_text = f"Match Details:\n\n" \
                       f"Home Team: {match['homeTeam']['name']}\n" \
                       f"Away Team: {match['awayTeam']['name']}\n" \
                       f"Date and Time: {match['utcDate']}\n"

        QMessageBox.information(self, "Match Details", details_text, QMessageBox.Ok)

    def show_match_details(self, checkbox, match, event):
        if event.type() == QEvent.MouseButtonDblClick:
        # Handle double-click
            details_text = f"Match Details:\n\n" \
                f"Home Team: {match['homeTeam']['name']}\n" \
                f"Away Team: {match['awayTeam']['name']}\n" \
                f"Date and Time: {match['utcDate']}\n"

        QMessageBox.information(self, "Match Details", details_text, QMessageBox.Ok)


    def init_ui(self):
        # UI Elements
        self.fixtures_label = QLabel('Fixtures:')
        self.fixtures_text = QTextEdit()
        self.fixtures_text.setReadOnly(True)

        self.refresh_button = QPushButton('Refresh Fixtures')
        self.refresh_button.clicked.connect(self.refresh_fixtures)

        self.print_selected_button = QPushButton('Print Selected')
        self.print_selected_button.clicked.connect(self.print_selected_matches)

        self.export_selected_button = QPushButton('Export Selected')
        self.export_selected_button.clicked.connect(self.export_selected_matches)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.fixtures_label)
        layout.addWidget(self.fixtures_text)
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.print_selected_button)
        layout.addWidget(self.export_selected_button)

        self.setLayout(layout)

        # Set up the main window
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('Fixture Display App')

        # Display fixtures initially
        self.refresh_fixtures()

    def refresh_fixtures(self):
        premier_league_id = 2021  # Premier League competition ID
        upcoming_fixtures = self.get_fixtures_data("SCHEDULED", premier_league_id)
        played_fixtures = self.get_fixtures_data("FINISHED", premier_league_id)

        if upcoming_fixtures is not None and played_fixtures is not None:
            self.display_fixtures(upcoming_fixtures, played_fixtures)
        else:
            self.fixtures_text.setPlainText('Error fetching fixtures data.')

    def get_fixtures_data(self, status, competition_id):
        base_url = f"https://api.football-data.org/v2/competitions/{competition_id}/matches"
        headers = {"X-Auth-Token": self.api_key}

        try:
            response = requests.get(base_url, headers=headers, params={"status": status})
            response.raise_for_status()  # Raise an exception for bad responses (4xx and 5xx)
            data = response.json()

            if response.status_code == 200:
                return data.get("matches", [])
            else:
                print(f"Error fetching fixtures data: {response.status_code}")
                return None
        except requests.exceptions.RequestException as err:
            print(f"Request error occurred: {err}")
            return None

    def display_fixtures(self, upcoming_fixtures, played_fixtures):
        self.selected_matches = []  # Reset selected matches on refresh
        fixtures_text = "Upcoming Fixtures:\n"
        fixtures_text += self.format_fixtures(upcoming_fixtures)

        fixtures_text += "\nPlayed Fixtures:\n"
        fixtures_text += self.format_fixtures(played_fixtures)

        self.fixtures_text.setPlainText(fixtures_text)

    def format_fixtures(self, fixtures_data):
        formatted_text = ""
        for match in fixtures_data:
            home_team = match["homeTeam"]["name"]
            away_team = match["awayTeam"]["name"]
            date_time = match["utcDate"]

            # Create a checkbox for each match
            checkbox = QCheckBox(f"{home_team} vs {away_team} - {date_time}")
            formatted_text += checkbox.text() + '\n'

            # Connect the stateChanged signal to the checkbox_clicked method
            checkbox.stateChanged.connect(lambda state, checkbox=checkbox, match=match: self.checkbox_clicked(state, checkbox, match))

            # Connect the doubleClicked signal to the show_match_details method
            checkbox.clicked.connect(lambda state, checkbox=checkbox, match=match: self.checkbox_clicked(state, checkbox, match))

        return formatted_text

if __name__ == '__main__':
    api_key = "6c2abd315f4e40d084d4ae4c6fae2ff6"  # Replace with your actual API key
    app = QApplication(sys.argv)
    main_window = FixtureDisplayApp(api_key)
    main_window.show()
    sys.exit(app.exec_())

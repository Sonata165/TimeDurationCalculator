import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from datetime import datetime, timedelta

class TimeDurationCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Create widgets for time
        self.start_label = QLabel('Start Time (HH:MM):', self)
        self.start_input = QLineEdit(self)
        self.end_label = QLabel('End Time (HH:MM):', self)
        self.end_input = QLineEdit(self)
        self.calculate_button = QPushButton('Calculate Duration', self)
        self.result_label = QLabel('Duration: ', self)

        # Set default start time to current time in HH:MM format
        self.start_input.setText(datetime.now().strftime('%H:%M'))

        # Create widgets for date
        self.start_date_label = QLabel('Start Date (YY/MM/DD):', self)
        self.start_date_input = QLineEdit(self)
        self.end_date_label = QLabel('End Date (YY/MM/DD):', self)
        self.end_date_input = QLineEdit(self)
        self.calculate_date_button = QPushButton('Calculate Date Duration', self)
        self.result_date_label = QLabel('Date Duration: ', self)

        # Set default start and end date to today's date in YY/MM/DD format
        today_date_str = datetime.now().strftime('%y/%m/%d')
        self.start_date_input.setText(today_date_str)
        self.end_date_input.setText(today_date_str)

        # Create widgets for current time to target date/time calculation
        # self.target_datetime_label = QLabel('Quit Time (YY/MM/DD HH:MM):', self)
        # self.target_datetime_input = QLineEdit(self)
        # self.calculate_target_button = QPushButton('Calculate Current to Quit Duration', self)
        self.quit_dur_label = QLabel('Current to Quit Duration: ', self)

        # Set quit date
        quit_time = '24/12/01 12:00'
        self.quit_time = quit_time

        # Layout
        layout = QVBoxLayout()
        
        # Time widgets
        layout.addWidget(self.start_label)
        layout.addWidget(self.start_input)
        layout.addWidget(self.end_label)
        layout.addWidget(self.end_input)
        layout.addWidget(self.calculate_button)
        layout.addWidget(self.result_label)

        # Add spacing between time and date sections
        layout.addSpacing(20)  # Adds 20 pixels of space

        # Date widgets
        layout.addWidget(self.start_date_label)
        layout.addWidget(self.start_date_input)
        layout.addWidget(self.end_date_label)
        layout.addWidget(self.end_date_input)
        layout.addWidget(self.calculate_date_button)
        layout.addWidget(self.result_date_label)

        # Add spacing between date and target datetime sections
        layout.addSpacing(20)  # Adds 20 pixels of space

        # Current to target datetime widgets
        layout.addWidget(self.quit_dur_label)

        self.setLayout(layout)

        # Connect events for time
        self.calculate_button.clicked.connect(self.calculate_duration)
        self.end_input.returnPressed.connect(self.calculate_duration)

        # Auto-add colon when inputting time
        self.start_input.textChanged.connect(self.auto_add_colon)
        self.end_input.textChanged.connect(self.auto_add_colon)

        # Connect events for date
        self.calculate_date_button.clicked.connect(self.calculate_date_duration)
        self.end_date_input.returnPressed.connect(self.calculate_date_duration)

        # Auto-add '/' when inputting date
        self.start_date_input.textChanged.connect(self.auto_add_slash)
        self.end_date_input.textChanged.connect(self.auto_add_slash)

        # Calculate the initial duration for the target datetime
        self.calculate_target_duration()

        # Window properties
        self.setWindowTitle('Duration Calculator')
        self.setGeometry(100, 100, 400, 400)

    def auto_add_colon(self, text):
        if len(text) == 2 and ':' not in text:
            self.sender().setText(text + ':')

    def auto_add_slash(self, text):
        if len(text) == 2 or len(text) == 5:
            if '/' not in text[-1]:  # Add '/' after YY or MM if not already there
                self.sender().setText(text + '/')

    def calculate_duration(self):
        start_time_str = self.start_input.text()
        end_time_str = self.end_input.text()

        try:
            # Parse the input times
            start_time = datetime.strptime(start_time_str, '%H:%M')
            end_time = datetime.strptime(end_time_str, '%H:%M')

            # Handle overnight durations
            if end_time < start_time:
                end_time = end_time.replace(day=start_time.day + 1)

            # Calculate the duration
            duration = end_time - start_time
            duration_minutes = int(duration.total_seconds() / 60)
            duration_hours = duration_minutes // 60
            remaining_minutes = duration_minutes % 60

            # Display the result
            self.result_label.setText(
                f'Duration: {duration_hours:02}:{remaining_minutes:02} ({duration_minutes} minutes)'
            )
        except ValueError:
            self.result_label.setText('Error: Please enter the time in HH:MM format.')

    def calculate_date_duration(self):
        start_date_str = self.start_date_input.text()
        end_date_str = self.end_date_input.text()

        try:
            # Parse the input dates
            start_date = datetime.strptime(start_date_str, '%y/%m/%d')
            end_date = datetime.strptime(end_date_str, '%y/%m/%d')

            # Handle year wraparound if necessary
            if end_date < start_date:
                end_date = end_date.replace(year=start_date.year + 1)

            # Calculate the date duration
            date_duration = end_date - start_date
            total_days = date_duration.days

            # Display the result
            self.result_date_label.setText(f'Date Duration: {total_days} days')
        except ValueError:
            self.result_date_label.setText('Error: Please enter the date in YY/MM/DD format.')

    def calculate_target_duration(self):
        target_datetime_str = self.quit_time

        try:
            # Parse the input target datetime
            target_datetime = datetime.strptime(target_datetime_str, '%y/%m/%d %H:%M')
            current_datetime = datetime.now()

            # Calculate the duration from current time to target time
            duration =  current_datetime - target_datetime

            total_seconds = duration.total_seconds()
            duration_days = total_seconds / 86400
            duration_hours = total_seconds / 3600

            # Display the result
            self.quit_dur_label.setText(
                f'Current to Quit Duration: {duration_days:.2f} days ({duration_hours:.2f} hours)'
            )
        except ValueError:
            self.quit_dur_label.setText('Error: Please enter the date in YY/MM/DD HH:MM format.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = TimeDurationCalculator()
    calculator.show()
    sys.exit(app.exec_())

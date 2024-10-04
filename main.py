import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from datetime import datetime

class TimeDurationCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Create widgets
        self.start_label = QLabel('Start Time (HH:MM):', self)
        self.start_input = QLineEdit(self)
        self.end_label = QLabel('End Time (HH:MM):', self)
        self.end_input = QLineEdit(self)
        self.calculate_button = QPushButton('Calculate Duration', self)
        self.result_label = QLabel('Duration: ', self)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.start_label)
        layout.addWidget(self.start_input)
        layout.addWidget(self.end_label)
        layout.addWidget(self.end_input)
        layout.addWidget(self.calculate_button)
        layout.addWidget(self.result_label)
        self.setLayout(layout)

        # Set up button click event and enter key event
        self.calculate_button.clicked.connect(self.calculate_duration)
        self.end_input.returnPressed.connect(self.calculate_duration)

        # Window properties
        self.setWindowTitle('Time Duration Calculator')
        self.setGeometry(100, 100, 300, 200)

    def calculate_duration(self):
        start_time_str = self.start_input.text()
        end_time_str = self.end_input.text()

        try:
            # Parse the input times
            start_time = datetime.strptime(start_time_str, '%H:%M')
            end_time = datetime.strptime(end_time_str, '%H:%M')

            # Calculate the duration
            if end_time < start_time:
                end_time = end_time.replace(day=start_time.day + 1)  # Handle overnight duration

            duration = end_time - start_time
            duration_minutes = int(duration.total_seconds() / 60)
            duration_hours = duration_minutes // 60
            remaining_minutes = duration_minutes % 60

            # Display the result in the result label
            self.result_label.setText(f'Duration: {duration_hours:02}:{remaining_minutes:02} ({duration_minutes} minutes)')
        except ValueError:
            self.result_label.setText('Error: Please enter the time in HH:MM format.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = TimeDurationCalculator()
    calculator.show()
    sys.exit(app.exec_())

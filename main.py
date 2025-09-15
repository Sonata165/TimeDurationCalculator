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
        # Set default end time to 17:45
        self.end_input.setText('19:00')

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
        # self.quit_dur_label = QLabel('Current to Quit Duration: ', self)

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
        # Move break time input here
        self.pomo_break_label = QLabel('Break Time (HH:MM):', self)
        self.pomo_break_input = QLineEdit(self)
        self.pomo_break_input.setText('2:00')
        layout.addWidget(self.pomo_break_label)
        layout.addWidget(self.pomo_break_input)
        layout.addWidget(self.calculate_button)
        layout.addWidget(self.result_label)

        # Pomodoro widgets (remove break input from here)
        self.pomo_gtd_label = QLabel('Pomos for GTD (p):', self)
        self.pomo_gtd_input = QLineEdit(self)
        self.pomo_gtd_input.setText('1')
        self.pomo_eff_label = QLabel('Efficiency Ratio:', self)
        self.pomo_eff_input = QLineEdit(self)
        self.pomo_eff_input.setText('0.85')
        self.pomo_main_label = QLabel('Main Ratio:', self)
        self.pomo_main_input = QLineEdit(self)
        self.pomo_main_input.setText('0.65')
        self.pomo_calc_button = QPushButton('Calculate Pomodoros', self)
        self.pomo_result_label = QLabel('Pomodoro Calculation: ', self)

        layout.addSpacing(10)
        layout.addWidget(self.pomo_gtd_label)
        layout.addWidget(self.pomo_gtd_input)
        layout.addWidget(self.pomo_eff_label)
        layout.addWidget(self.pomo_eff_input)
        layout.addWidget(self.pomo_main_label)
        layout.addWidget(self.pomo_main_input)
        layout.addWidget(self.pomo_calc_button)
        layout.addWidget(self.pomo_result_label)
        layout.addSpacing(20)

        # Connect pomodoro calculation button
        self.pomo_calc_button.clicked.connect(self.calculate_pomodoro)

        # Date widgets
        layout.addWidget(self.start_date_label)
        layout.addWidget(self.start_date_input)
        layout.addWidget(self.end_date_label)
        layout.addWidget(self.end_date_input)
        layout.addWidget(self.calculate_date_button)
        layout.addWidget(self.result_date_label)

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

        # # Calculate the initial duration for the target datetime
        # self.calculate_target_duration()

        # Window properties
        self.setWindowTitle('Duration Calculator')
        self.setGeometry(100, 100, 400, 400)

        # Automatically calculate duration and pomodoro on startup
        self.calculate_duration()
        self.calculate_pomodoro()

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
        break_time_str = self.pomo_break_input.text()
        try:
            # Parse the input times
            start_time = datetime.strptime(start_time_str, '%H:%M')
            end_time = datetime.strptime(end_time_str, '%H:%M')
            if end_time < start_time:
                end_time = end_time.replace(day=start_time.day + 1)
            duration = end_time - start_time
            duration_minutes = int(duration.total_seconds() / 60)
            duration_hours = duration_minutes // 60
            remaining_minutes = duration_minutes % 60
            # Deduct break time
            break_time = datetime.strptime(break_time_str, '%H:%M')
            break_minutes = break_time.hour * 60 + break_time.minute
            duration_minutes_deducted = duration_minutes - break_minutes
            duration_hours_deducted = duration_minutes_deducted // 60
            remaining_minutes_deducted = duration_minutes_deducted % 60
            # Display both total and deducted durations
            self.result_label.setText(
                f"Total Duration: {duration_hours:02}:{remaining_minutes:02} ({duration_minutes} min)\n"
                f"Deducted Break: {duration_hours_deducted:02}:{remaining_minutes_deducted:02} ({duration_minutes_deducted} min)"
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

    def calculate_pomodoro(self):
        # Get start and end time for the day
        start_time_str = self.start_input.text()
        end_time_str = self.end_input.text()
        break_time_str = self.pomo_break_input.text()
        gtd_pomo_str = self.pomo_gtd_input.text()
        try:
            start_time = datetime.strptime(start_time_str, '%H:%M')
            end_time = datetime.strptime(end_time_str, '%H:%M')
            if end_time < start_time:
                end_time = end_time.replace(day=start_time.day + 1)
            total_minutes = int((end_time - start_time).total_seconds() / 60)

            # Deduct break time
            break_time = datetime.strptime(break_time_str, '%H:%M')
            break_minutes = break_time.hour * 60 + break_time.minute
            work_minutes = total_minutes - break_minutes
            # Efficiency ratio
            try:
                eff_ratio = float(self.pomo_eff_input.text())
            except ValueError:
                eff_ratio = 0.85
            eff_minutes = int(work_minutes * eff_ratio)

            # Pomodoros (total should include GTD pomos)
            pomo_count = eff_minutes // 30

            # Deduct GTD pomos (1 pomo = 30 min)
            try:
                gtd_pomo = int(gtd_pomo_str)
            except ValueError:
                gtd_pomo = 1
            gtd_minutes = gtd_pomo * 30
            eff_minutes_after_gtd = eff_minutes - gtd_minutes
            if eff_minutes_after_gtd < 0:
                eff_minutes_after_gtd = 0

            # Main ratio
            try:
                main_ratio = float(self.pomo_main_input.text())
            except ValueError:
                main_ratio = 0.65
            main_minutes = int(eff_minutes_after_gtd * main_ratio)
            main_pomo = main_minutes // 30
            remain_pomo = pomo_count - gtd_pomo - main_pomo
            self.pomo_result_label.setText(
                "Pomodoro Calculation:\n"
                f"    Efficient Time:  \t{eff_minutes} min\n"
                f"    Total #Pomo:     \t{pomo_count}p\n"
                f"     - GTD pomos:    \t{gtd_pomo:>2}p\n"
                f"     - Main Project: \t{main_pomo:>2}p\n"
                f"     - Remaining:    \t{remain_pomo:>2}p\n"
            )
            # labels = ["GTD pomos", "Main Project", "Remaining"]
            # values = [gtd_pomo, main_pomo, remain_pomo]

            # label_width = max(len(lbl) for lbl in labels)
            # value_width = max(len(str(v)) + 1 for v in values)  # +1 给 'p'

            # lines = [
            #     f"     - {label:<{label_width}} : {f'{value}p':>{value_width}}"
            #     for label, value in zip(labels, values)
            # ]

            # self.pomo_result_label.setText(
            #     "Pomodoro Calculation:\n"
            #     f"    Efficient Time: \t{eff_minutes} min\n"
            #     f"    Total #Pomo: \t{pomo_count}p\n"
            #     + "\n".join(lines)
            # )
        except Exception:
            self.pomo_result_label.setText('Error: Please check your time and input formats.')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = TimeDurationCalculator()
    calculator.show()
    sys.exit(app.exec_())

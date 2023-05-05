from datetime import datetime

class DateSelection:
    def __init__(self):
        self.start_date = None
        self.end_date = None

    # Validate the user input for date in the YYYY-MM-DD format
    def _input_validation(self, date_str):
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    # Get user input for a date and validate it
    def input_date(self, prompt):
        while True:
            date_str = input(prompt)
            if self._input_validation(date_str):
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
                return date
            else:
                print("Invalid date format. Please use the YYYY-MM-DD format.")

    # Allow the user to select start and end dates for the analysis
    def select_dates(self):
        while self.start_date is None:
            self.start_date = self.input_date("Enter the start date (YYYY-MM-DD): ")

        while self.end_date is None:
            self.end_date = self.input_date("Enter the end date (YYYY-MM-DD): ")

        if self.start_date > self.end_date:
            print("Error: Start date cannot be later than the end date. Please try again.")
            self.start_date = None
            self.end_date = None
            self.select_dates()

        return self.start_date, self.end_date
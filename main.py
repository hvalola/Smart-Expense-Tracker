# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import csv
import os

from utils.logger import get_logger


logger = get_logger("smart_expense_tracker")


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    logger.info("Hi, %s", name)  # Press Ctrl+F8 to toggle the breakpoint.


def capture_input():
    """Capture expense details from the terminal."""
    expense = {
        'amount': input("Amount: "),
        'date': input("Date: "),
        'description': input("Description: "),
        'payment_method': input("Payment Method: "),
        'currency': input("Currency: "),
        'merchant': input("Merchant: "),
        'location': input("Location: ")
    }
    return expense


def save_to_csv(expense, filename='expenses.csv'):
    """Save expense data to CSV file in append mode."""
    file_exists = os.path.isfile(filename)

    try:
        with open(filename, 'a', newline='') as csvfile:
            fieldnames = ['amount', 'date', 'description', 'payment_method', 'currency', 'merchant', 'location']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write header only if file doesn't exist
            if not file_exists:
                writer.writeheader()

            writer.writerow(expense)

        logger.info("Expense saved to %s", filename)
    except OSError as exc:
        logger.error("Failed to save expense to %s: %s", filename, exc)
        raise


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    expenses = capture_input()
    logger.info("Captured Expense Details")
    for key, value in expenses.items():
        logger.debug("%s: %s", key.capitalize(), value)
    
    # Save to CSV file
    save_to_csv(expenses)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

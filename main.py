# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import csv
import os
import json

from utils.logger import get_logger
from utils.helpers import (
    validate_amount,
    validate_date,
    validate_description,
    validate_payment_method,
    validate_currency,
    validate_merchant,
    validate_location,
    ValidationError,
    cleanse_expense_record,
    cleanse_dataset
)


logger = get_logger("smart_expense_tracker")


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    logger.info("Hi, %s", name)  # Press Ctrl+F8 to toggle the breakpoint.


def get_validated_input(prompt: str, validator_func) -> str:
    """
    Get input from user with validation.
    
    Args:
        prompt: Prompt to display to user
        validator_func: Function to validate the input
        
    Returns:
        str: Validated input
    """
    while True:
        try:
            user_input = input(prompt)
            validated_value = validator_func(user_input)
            return validated_value
        except ValidationError as e:
            logger.warning("Validation error: %s", str(e))
            print(f"Error: {str(e)}. Please try again.")


def capture_input():
    """Capture expense details from the terminal with validation."""
    print("\n--- Enter Expense Details ---")
    expense = {
        'amount': str(get_validated_input("Amount: ", validate_amount)),
        'date': get_validated_input("Date (YYYY-MM-DD or DD/MM/YYYY): ", validate_date),
        'description': get_validated_input("Description: ", validate_description),
        'payment_method': get_validated_input("Payment Method (cash/credit_card/debit_card/bank_transfer/digital_wallet/other): ", validate_payment_method),
        'currency': get_validated_input("Currency (ISO 4217 code, e.g., USD): ", validate_currency),
        'merchant': get_validated_input("Merchant: ", validate_merchant),
        'location': get_validated_input("Location: ", validate_location)
    }
    print()
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


def load_expenses_from_csv(filename='expenses.csv') -> list:
    """
    Load expenses from CSV file.
    
    Args:
        filename: CSV file to read
        
    Returns:
        list: List of expense dictionaries
    """
    expenses = []
    
    if not os.path.isfile(filename):
        logger.warning("File %s not found", filename)
        return expenses
    
    try:
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            expenses = list(reader)
        logger.info("Loaded %d expenses from %s", len(expenses), filename)
    except OSError as exc:
        logger.error("Failed to read %s: %s", filename, exc)
    
    return expenses


def cleanse_and_report(filename='expenses.csv', output_file='cleansed_expenses.json'):
    """
    Cleanse expense data from CSV and generate quality report.
    
    Args:
        filename: Source CSV file
        output_file: Output file for cleansed data
    """
    print("\n--- Cleansing Expense Data ---")
    
    # Load raw data
    expenses = load_expenses_from_csv(filename)
    
    if not expenses:
        print("No expenses to cleanse.")
        return
    
    # Cleanse dataset
    cleansed_records, quality_report = cleanse_dataset(expenses)
    
    # Display report
    print("\nData Quality Report:")
    print(f"  Total Records: {quality_report['total_records']}")
    print(f"  Valid Records: {quality_report['valid_records']}")
    print(f"  Records with Missing Fields: {quality_report['records_with_missing_fields']}")
    print(f"  Invalid Records: {quality_report['invalid_records']}")
    
    if quality_report['issues']:
        print("\nIssues Found:")
        for issue in quality_report['issues'][:10]:  # Show first 10 issues
            print(f"  - {issue}")
    
    # Save cleansed data
    try:
        with open(output_file, 'w') as f:
            json.dump({
                'cleansed_records': cleansed_records,
                'quality_report': quality_report
            }, f, indent=2)
        print(f"\nCleansed data saved to {output_file}")
        logger.info("Cleansed %d valid records to %s", len(cleansed_records), output_file)
    except OSError as exc:
        logger.error("Failed to save cleansed data: %s", exc)
    
    print()


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

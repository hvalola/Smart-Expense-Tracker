"""Helper functions for data validation and processing."""

import re
from datetime import datetime


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def validate_amount(amount: str) -> float:
    """
    Validate and convert amount to float.
    
    Args:
        amount: String representation of the amount
        
    Returns:
        float: Validated amount
        
    Raises:
        ValidationError: If amount is invalid
    """
    amount = amount.strip()
    
    if not amount:
        raise ValidationError("Amount cannot be empty")
    
    try:
        amount_float = float(amount)
    except ValueError:
        raise ValidationError(f"Amount must be a valid number, got '{amount}'")
    
    if amount_float <= 0:
        raise ValidationError("Amount must be greater than 0")
    
    if amount_float > 999999.99:
        raise ValidationError("Amount exceeds maximum allowed value (999999.99)")
    
    return amount_float


def validate_date(date: str) -> str:
    """
    Validate date format (YYYY-MM-DD or DD/MM/YYYY).
    
    Args:
        date: String representation of the date
        
    Returns:
        str: Validated date in YYYY-MM-DD format
        
    Raises:
        ValidationError: If date is invalid
    """
    date = date.strip()
    
    if not date:
        raise ValidationError("Date cannot be empty")
    
    # Try YYYY-MM-DD format
    try:
        parsed_date = datetime.strptime(date, "%Y-%m-%d")
        return parsed_date.strftime("%Y-%m-%d")
    except ValueError:
        pass
    
    # Try DD/MM/YYYY format
    try:
        parsed_date = datetime.strptime(date, "%d/%m/%Y")
        return parsed_date.strftime("%Y-%m-%d")
    except ValueError:
        pass
    
    raise ValidationError("Date must be in YYYY-MM-DD or DD/MM/YYYY format")


def validate_description(description: str) -> str:
    """
    Validate description.
    
    Args:
        description: Description text
        
    Returns:
        str: Validated description
        
    Raises:
        ValidationError: If description is invalid
    """
    description = description.strip()
    
    if not description:
        raise ValidationError("Description cannot be empty")
    
    if len(description) > 255:
        raise ValidationError("Description must not exceed 255 characters")
    
    return description


def validate_payment_method(method: str) -> str:
    """
    Validate payment method.
    
    Args:
        method: Payment method
        
    Returns:
        str: Validated payment method
        
    Raises:
        ValidationError: If payment method is invalid
    """
    valid_methods = ['cash', 'credit_card', 'debit_card', 'bank_transfer', 'digital_wallet', 'other']
    method = method.strip().lower()
    
    if not method:
        raise ValidationError("Payment method cannot be empty")
    
    if method not in valid_methods:
        raise ValidationError(f"Invalid payment method. Allowed: {', '.join(valid_methods)}")
    
    return method


def validate_currency(currency: str) -> str:
    """
    Validate currency code (ISO 4217).
    
    Args:
        currency: Currency code
        
    Returns:
        str: Validated currency code in uppercase
        
    Raises:
        ValidationError: If currency is invalid
    """
    common_currencies = ['USD', 'EUR', 'GBP', 'JPY', 'AUD', 'CAD', 'CHF', 'CNY', 'INR', 'MXN']
    currency = currency.strip().upper()
    
    if not currency:
        raise ValidationError("Currency cannot be empty")
    
    if len(currency) != 3 or not currency.isalpha():
        raise ValidationError("Currency must be a 3-letter ISO 4217 code (e.g., USD, EUR)")
    
    if currency not in common_currencies:
        raise ValidationError(f"Currency '{currency}' not in common currencies. Common: {', '.join(common_currencies)}")
    
    return currency


def validate_merchant(merchant: str) -> str:
    """
    Validate merchant name.
    
    Args:
        merchant: Merchant name
        
    Returns:
        str: Validated merchant name
        
    Raises:
        ValidationError: If merchant is invalid
    """
    merchant = merchant.strip()
    
    if not merchant:
        raise ValidationError("Merchant cannot be empty")
    
    if len(merchant) > 100:
        raise ValidationError("Merchant name must not exceed 100 characters")
    
    return merchant


def validate_location(location: str) -> str:
    """
    Validate location.
    
    Args:
        location: Location name
        
    Returns:
        str: Validated location
        
    Raises:
        ValidationError: If location is invalid
    """
    location = location.strip()
    
    if not location:
        raise ValidationError("Location cannot be empty")
    
    if len(location) > 150:
        raise ValidationError("Location must not exceed 150 characters")
    
    return location


# ============================================================================
# Data Cleansing Functions
# ============================================================================

def cleanse_amount(amount) -> float:
    """
    Cleanse amount data by converting to float and rounding to 2 decimals.
    
    Args:
        amount: Amount value (can be string or numeric)
        
    Returns:
        float: Cleansed amount rounded to 2 decimal places
    """
    try:
        amount_float = float(str(amount).strip())
        return round(amount_float, 2)
    except (ValueError, AttributeError):
        return None


def cleanse_date(date_str: str) -> str:
    """
    Cleanse date by standardizing to YYYY-MM-DD format.
    
    Args:
        date_str: Date string
        
    Returns:
        str: Standardized date or None if invalid
    """
    date_str = str(date_str).strip()
    
    # Try common date formats
    formats = ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y", "%Y/%m/%d"]
    
    for date_format in formats:
        try:
            parsed_date = datetime.strptime(date_str, date_format)
            return parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            continue
    
    return None


def cleanse_text(text: str, max_length: int = None) -> str:
    """
    Cleanse text by trimming whitespace and normalizing spaces.
    
    Args:
        text: Text to cleanse
        max_length: Optional maximum length to truncate
        
    Returns:
        str: Cleansed text
    """
    if not isinstance(text, str):
        text = str(text)
    
    # Strip leading/trailing whitespace and normalize internal spaces
    text = ' '.join(text.strip().split())
    
    # Remove special characters but keep alphanumeric and basic punctuation
    text = re.sub(r'[^\w\s.,&\-]', '', text)
    
    if max_length and len(text) > max_length:
        text = text[:max_length].strip()
    
    return text


def cleanse_payment_method(method: str) -> str:
    """
    Cleanse payment method by standardizing format.
    
    Args:
        method: Payment method string
        
    Returns:
        str: Standardized payment method or None if invalid
    """
    if not isinstance(method, str):
        return None
    
    method = method.strip().lower()
    
    # Normalize variations
    normalizations = {
        'cash': 'cash',
        'cc': 'credit_card',
        'credit': 'credit_card',
        'credit_card': 'credit_card',
        'creditcard': 'credit_card',
        'dc': 'debit_card',
        'debit': 'debit_card',
        'debit_card': 'debit_card',
        'debitcard': 'debit_card',
        'transfer': 'bank_transfer',
        'bank_transfer': 'bank_transfer',
        'wire': 'bank_transfer',
        'wallet': 'digital_wallet',
        'digital_wallet': 'digital_wallet',
        'mobile': 'digital_wallet',
        'paypal': 'digital_wallet',
        'other': 'other'
    }
    
    return normalizations.get(method, None)


def cleanse_currency(currency: str) -> str:
    """
    Cleanse currency code by standardizing to uppercase ISO 4217 format.
    
    Args:
        currency: Currency code
        
    Returns:
        str: Standardized currency code or None if invalid
    """
    if not isinstance(currency, str):
        return None
    
    currency = currency.strip().upper()
    
    if len(currency) == 3 and currency.isalpha():
        return currency
    
    return None


def cleanse_merchant(merchant: str) -> str:
    """
    Cleanse merchant name by standardizing format.
    
    Args:
        merchant: Merchant name
        
    Returns:
        str: Cleansed merchant name
    """
    return cleanse_text(merchant, max_length=100)


def cleanse_location(location: str) -> str:
    """
    Cleanse location by standardizing format.
    
    Args:
        location: Location name
        
    Returns:
        str: Cleansed location
    """
    return cleanse_text(location, max_length=150)


def cleanse_description(description: str) -> str:
    """
    Cleanse description by standardizing format.
    
    Args:
        description: Description text
        
    Returns:
        str: Cleansed description
    """
    return cleanse_text(description, max_length=255)


def cleanse_expense_record(expense: dict) -> dict:
    """
    Cleanse an entire expense record for analysis.
    
    Args:
        expense: Dictionary containing expense data
        
    Returns:
        dict: Cleansed expense record
    """
    cleansed = {
        'amount': cleanse_amount(expense.get('amount')),
        'date': cleanse_date(expense.get('date')),
        'description': cleanse_description(expense.get('description')),
        'payment_method': cleanse_payment_method(expense.get('payment_method')),
        'currency': cleanse_currency(expense.get('currency')),
        'merchant': cleanse_merchant(expense.get('merchant')),
        'location': cleanse_location(expense.get('location'))
    }
    
    return cleansed


def cleanse_dataset(expenses: list) -> tuple[list, dict]:
    """
    Cleanse a list of expense records and return cleansed data with quality report.
    
    Args:
        expenses: List of expense dictionaries
        
    Returns:
        tuple: (cleansed_records, quality_report)
    """
    cleansed_records = []
    quality_report = {
        'total_records': len(expenses),
        'valid_records': 0,
        'invalid_records': 0,
        'records_with_missing_fields': 0,
        'issues': []
    }
    
    for idx, expense in enumerate(expenses):
        cleansed = cleanse_expense_record(expense)
        
        # Check for None values (invalid fields)
        none_count = sum(1 for v in cleansed.values() if v is None)
        
        if none_count == 0:
            quality_report['valid_records'] += 1
            cleansed_records.append(cleansed)
        elif none_count < len(cleansed):
            quality_report['records_with_missing_fields'] += 1
            cleansed_records.append(cleansed)
        else:
            quality_report['invalid_records'] += 1
            quality_report['issues'].append(f"Row {idx + 1}: All fields invalid")
    
    return cleansed_records, quality_report

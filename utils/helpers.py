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

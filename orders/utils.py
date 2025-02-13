import re
from datetime import datetime


def validate_card_details(card_number: str, exp_date: str, cvc: str):
    """Valida el formato de la tarjeta de crédito/débito, su fecha de caducidad y su CVC."""
    card_pattern = r'\d{4}-\d{4}-\d{4}-\d{4}'
    date_pattern = r'\d{2}/\d{4}'
    cvc_pattern = r'\d{3}'

    if not re.fullmatch(card_pattern, card_number):
        return 'Invalid card number'
    if not re.fullmatch(date_pattern, exp_date):
        return 'Invalid expiration date'
    if not re.fullmatch(cvc_pattern, cvc):
        return 'Invalid CVC'

    exp_month, exp_year = map(int, exp_date.split('/'))
    current_year = datetime.now().year
    current_month = datetime.now().month

    if exp_year < current_year or (exp_year == current_year and exp_month < current_month):
        return 'Card expired'

    return None

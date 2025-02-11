import re
from datetime import datetime

from users.models import Token

UUID_PATTERN = (
    r'Bearer (?P<token>[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12})'
)


def extract_token(auth_header):
    if not auth_header:
        return None
    match = re.fullmatch(UUID_PATTERN, auth_header)
    return match['token'] if match else None


def get_authenticated_user(token):
    try:
        return Token.objects.get(key=token).user
    except Token.DoesNotExist:
        return None


def validate_required_fields(data, required_fields):
    return all(field in data for field in required_fields)


def validate_card_details(card_number, exp_date, cvc):
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

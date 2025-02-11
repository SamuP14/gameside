import re

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

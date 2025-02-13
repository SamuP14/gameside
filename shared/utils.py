import re

from users.models import Token

UUID_PATTERN = (
    r'Bearer (?P<token>[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12})'
)


def extract_token(auth_header: str):
    """Extrae el 'Bearer Token' de la cabecera de la petición HTTP recibida como parámetro."""
    if not auth_header:
        return None
    match = re.fullmatch(UUID_PATTERN, auth_header)
    return match['token'] if match else None


def get_authenticated_user(token: str):
    """Comprueba que el token extraído exista en la base de datos y devuelve el usuario al que pertenece."""
    try:
        return Token.objects.get(key=token).user
    except Token.DoesNotExist:
        return None


def validate_required_fields(data, required_fields: list) -> bool:
    """Valida que los datos recibidos del 'Body' de la petición exista en la lista de campos requeridos."""
    return all(field in data for field in required_fields)

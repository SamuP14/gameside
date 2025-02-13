import json
from json.decoder import JSONDecodeError

from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from shared import utils
from shared.decorators import post_required


@csrf_exempt
@post_required
def auth(request):
    """Devuelve el token del usuario identificado por su nombre de usuario y contraseña."""
    try:
        data = json.loads(request.body)
    except JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)
    else:
        keys = ['username', 'password']

        if not utils.validate_required_fields(data, keys):
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        if user := authenticate(username=data['username'], password=data['password']):
            return JsonResponse({'token': user.user_token.key}, status=200)
        return JsonResponse({'error': 'Invalid credentials'}, status=401)

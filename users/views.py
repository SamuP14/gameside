import json
from json.decoder import JSONDecodeError

from django.contrib.auth.models import User
from django.http import JsonResponse

from shared.decorators import post_required


@post_required
def auth(request):
    try:
        data = json.loads(request.body)
    except JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)
    else:
        keys = ['username', 'password']

        for key in keys:
            if key not in data.keys():
                return JsonResponse({'error': 'Missing required fields'}, status=400)

        username = data['username']
        password = data['password']
        try:
            user = User.objects.get(username=username, password=password)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
        else:
            pass

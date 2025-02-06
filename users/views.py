import json
from json.decoder import JSONDecodeError

# from django.contrib.auth import authenticate
# from django.contrib.auth.models import User
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from shared.decorators import post_required
# from .models import Token
# @csrf_exempt
# @post_required
# def auth(request):
#     try:
#         data = json.loads(request.body)
#     except JSONDecodeError:
#         return JsonResponse({'error': 'Invalid JSON body'}, status=400)
#     else:
#         keys = ['username', 'password']
#         for key in keys:
#             if key not in data.keys():
#                 return JsonResponse({'error': 'Missing required fields'}, status=400)
#         username = data['username']
#         password = data['password']
#         try:
#             user = authenticate(username=username, password=password)
#         except User.DoesNotExist:
#             return JsonResponse({'error': 'Invalid credentials'}, status=401)
#         else:
#             token = Token.objects.get(user=user)
#             return JsonResponse({'token': token.key}, status=200)
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from shared.decorators import post_required


@csrf_exempt
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

        if user := authenticate(username=data['username'], password=data['password']):
            return JsonResponse({'token': user.user_token.key})
        return JsonResponse({'error': 'Invalid credentials'}, status=401)

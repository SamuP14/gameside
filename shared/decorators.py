from functools import wraps

from django.http import JsonResponse


def get_required(function):
    """Fuerza a que se utilize el método HTTP 'GET'."""

    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.method != 'GET':
            return JsonResponse({'error': 'Method not allowed'}, status=405)
        return function(request, *args, **kwargs)

    return wrap


def post_required(function):
    """Fuerza a que se utilize el método HTTP 'POST'."""

    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.method != 'POST':
            return JsonResponse({'error': 'Method not allowed'}, status=405)
        return function(request, *args, **kwargs)

    return wrap

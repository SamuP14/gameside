from django.http import JsonResponse

from .models import Platform
from .serializers import PlatformSerializer


def platform_list(request):
    if request.method == 'GET':
        platforms = Platform.objects.all()
        serializer = PlatformSerializer(platforms, request=request)
        return serializer.json_response()
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def platform_detail(request, platform_slug):
    if request.method == 'GET':
        try:
            platform = Platform.objects.get(slug=platform_slug)
        except Platform.DoesNotExist:
            return JsonResponse({'error': 'Platform not found'}, status=404)
        else:
            serializer = PlatformSerializer(platform, request=request)
            return serializer.json_response()
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

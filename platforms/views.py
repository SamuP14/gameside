from django.http import JsonResponse

from shared.decorators import get_required

from .models import Platform
from .serializers import PlatformSerializer


@get_required
def platform_list(request) -> str:
    """Lista todas las plataformas disponibles."""
    platforms = Platform.objects.all()
    serializer = PlatformSerializer(platforms, request=request)
    return serializer.json_response()


@get_required
def platform_detail(request, platform_slug: str) -> str:
    """Lista los detalles de una plataforma, buscada por su slug."""
    try:
        platform = Platform.objects.get(slug=platform_slug)
    except Platform.DoesNotExist:
        return JsonResponse({'error': 'Platform not found'}, status=404)
    else:
        serializer = PlatformSerializer(platform, request=request)
        return serializer.json_response()

from django.http import JsonResponse

from shared.decorators import get_required

from .models import Category
from .serializers import CategorySerializer


@get_required
def category_list(request) -> str:
    """Lista todas las categorías disponibles."""
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, request=request)
    return serializer.json_response()


@get_required
def category_detail(request, category_slug: str) -> str:
    """Lista los detalles de una categoría, buscada por su slug."""
    try:
        category = Category.objects.get(slug=category_slug)
    except Category.DoesNotExist:
        return JsonResponse({'error': 'Category not found'}, status=404)
    else:
        serializer = CategorySerializer(category, request=request)
        return serializer.json_response()

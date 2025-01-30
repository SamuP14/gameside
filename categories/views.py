from django.http import JsonResponse

from .models import Category
from .serializers import CategorySerializer


def category_list(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, request=request)
        return serializer.json_response()
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def category_detail(request, category_slug):
    if request.method == 'GET':
        try:
            category = Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            return JsonResponse({'error': 'Category not found'}, status=404)
        else:
            serializer = CategorySerializer(category, request=request)
            return serializer.json_response()
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

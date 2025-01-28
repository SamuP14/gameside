from django.http import JsonResponse
from django.shortcuts import render

from .models import Game, Review
from .serializers import GameSerializer, ReviewSerializer


def game_list(request):
    if request.method == 'GET':
        games = Game.objects.all()
        serializer = GameSerializer(games, request=request)
        return serializer.json_response()
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def game_detail(request, game_slug):
    if request.method == 'GET':
        game = Game.objects.filter(slug=game_slug)
        if game:
            serializer = GameSerializer(game)
            return serializer.json_response()
        else:
            return JsonResponse({'error': 'Game not found'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def review_list(request, game_slug):
    game = Game.objects.get(slug=game_slug)
    reviews = Review.objects.filter(game=game)
    serializer = ReviewSerializer(reviews)
    return serializer.json_response()


def add_review(request):
    return render(request)


def review_detail(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    serializer = ReviewSerializer(review)
    return serializer.json_response()

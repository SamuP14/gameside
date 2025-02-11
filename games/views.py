import json
from json.decoder import JSONDecodeError

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from categories.models import Category
from platforms.models import Platform
from shared import utils
from shared.decorators import get_required, post_required
from users.models import Token

from .models import Game, Review
from .serializers import GameSerializer, ReviewSerializer


@get_required
def game_list(request):
    platform = request.GET.get('platform', None)
    category = request.GET.get('category', None)

    games = Game.objects.all()

    if platform:
        platform_instance = Platform.objects.get(slug=platform)
        games = games.filter(platforms=platform_instance)
    if category:
        category_instance = Category.objects.get(slug=category)
        games = games.filter(category=category_instance)

    serializes_games = GameSerializer(games, request=request)

    return JsonResponse(serializes_games.serialize(), safe=False)


@get_required
def game_detail(request, game_slug):
    try:
        game = Game.objects.get(slug=game_slug)
    except Game.DoesNotExist:
        return JsonResponse({'error': 'Game not found'}, status=404)
    else:
        serializer = GameSerializer(game, request=request)
        return serializer.json_response()


@get_required
def review_list(request, game_slug):
    try:
        game = Game.objects.get(slug=game_slug)
    except Game.DoesNotExist:
        return JsonResponse({'error': 'Game not found'}, status=404)
    else:
        reviews = Review.objects.filter(game=game)
        serializer = ReviewSerializer(reviews, request=request)
        return serializer.json_response()


@get_required
def review_detail(request, review_pk):
    try:
        review = Review.objects.get(pk=review_pk)
    except Review.DoesNotExist:
        return JsonResponse({'error': 'Review not found'}, status=404)
    else:
        review = Review.objects.get(pk=review_pk)
        serializer = ReviewSerializer(review, request=request)
        return serializer.json_response()


@csrf_exempt
@post_required
def add_review(request, game_slug):
    try:
        data = json.loads(request.body)
    except JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)
    else:
        keys = ['rating', 'comment']

        if not utils.validate_required_fields(data, keys):
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        for key in keys:
            if key not in data.keys():
                return JsonResponse({'error': 'Missing required fields'}, status=400)

        token = utils.extract_token(request.headers.get('Authorization'))
        if not token:
            return JsonResponse({'error': 'Invalid authentication token'}, status=400)

        rating = data['rating']
        comment = data['comment']

        if rating < 1 or rating > 5:
            return JsonResponse({'error': 'Rating is out of range'}, status=400)

        user = utils.get_authenticated_user(token)
        if not user:
            return JsonResponse({'error': 'Unregistered authentication token'}, status=401)

        try:
            game = Game.objects.get(slug=game_slug)
        except Game.DoesNotExist:
            return JsonResponse({'error': 'Game not found'}, status=404)
        else:
            author = Token.objects.get(key=token).user
            review = Review.objects.create(rating=rating, comment=comment, game=game, author=author)
            return JsonResponse({'id': review.pk}, status=200)

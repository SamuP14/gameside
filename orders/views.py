import json
import re
from json.decoder import JSONDecodeError

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from games.models import Game
from games.serializers import GameSerializer
from shared.decorators import get_required, post_required
from users.models import Token

from .models import Order
from .serializers import OrderSerializer


@csrf_exempt
@post_required
def add_order(request):
    raw_token = request.headers.get('Authorization')
    uuid_pattern = r'Bearer (?P<token>[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12})'
    match = re.fullmatch(uuid_pattern, raw_token)

    if match:
        token = match['token']
        try:
            Token.objects.get(key=token)
        except Token.DoesNotExist:
            return JsonResponse({'error': 'Unregistered authentication token'}, status=401)
        else:
            user = Token.objects.get(key=token).user
            order = Order.objects.create(user=user)
            return JsonResponse({'id': order.pk}, status=200)
    else:
        return JsonResponse({'error': 'Invalid authentication token'}, status=400)


@get_required
def order_detail(request, order_pk):
    raw_token = request.headers.get('Authorization')
    uuid_pattern = r'Bearer (?P<token>[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12})'
    match = re.fullmatch(uuid_pattern, raw_token)
    if match:
        token = match['token']
        try:
            key = Token.objects.get(key=token)
        except Token.DoesNotExist:
            return JsonResponse({'error': 'Unregistered authentication token'}, status=401)
        else:
            user = key.user
            try:
                order = Order.objects.get(pk=order_pk)
            except Order.DoesNotExist:
                return JsonResponse({'error': 'Order not found'}, status=404)
            else:
                if user == order.user:
                    serializer = OrderSerializer(order, request=request)
                    return serializer.json_response()
                else:
                    return JsonResponse(
                        {'error': 'User is not the owner of requested order'}, status=403
                    )

    else:
        return JsonResponse({'error': 'Invalid authentication token'}, status=400)


@get_required
def order_game_list(request, order_pk):
    raw_token = request.headers.get('Authorization')
    uuid_pattern = r'Bearer (?P<token>[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12})'
    match = re.fullmatch(uuid_pattern, raw_token)
    if match:
        token = match['token']
        try:
            key = Token.objects.get(key=token)
        except Token.DoesNotExist:
            return JsonResponse({'error': 'Unregistered authentication token'}, status=401)
        else:
            user = key.user
            try:
                order = Order.objects.get(pk=order_pk)
            except Order.DoesNotExist:
                return JsonResponse({'error': 'Order not found'}, status=404)
            else:
                if user == order.user:
                    games = order.games.all()
                    serializer = GameSerializer(games, request=request)
                    return serializer.json_response()
                else:
                    return JsonResponse(
                        {'error': 'User is not the owner of requested order'}, status=403
                    )

    else:
        return JsonResponse({'error': 'Invalid authentication token'}, status=400)


@csrf_exempt
@post_required
def add_game_to_order(request, order_pk):
    try:
        data = json.loads(request.body)
    except JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)
    else:
        keys = ['game-slug']

        for key in keys:
            if key not in data.keys():
                return JsonResponse({'error': 'Missing required fields'}, status=400)

        raw_token = request.headers.get('Authorization')
        uuid_pattern = r'Bearer (?P<token>[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12})'
        match = re.fullmatch(uuid_pattern, raw_token)
        if match:
            token = match['token']
            game_slug = data['game-slug']
            try:
                key = Token.objects.get(key=token)
            except Token.DoesNotExist:
                return JsonResponse({'error': 'Unregistered authentication token'}, status=401)
            else:
                user = key.user
                try:
                    order = Order.objects.get(pk=order_pk)
                except Order.DoesNotExist:
                    return JsonResponse({'error': 'Order not found'}, status=404)
                else:
                    try:
                        game = Game.objects.get(slug=game_slug)
                    except Game.DoesNotExist:
                        return JsonResponse({'error': 'Game not found'}, status=404)
                    else:
                        game.rest_stock()
                        if user == order.user:
                            order.games.add(game)
                            return JsonResponse(
                                {'num-games-in-order': order.games.count()}, safe=False
                            )

                        else:
                            return JsonResponse(
                                {'error': 'User is not the owner of requested order'}, status=403
                            )
        else:
            return JsonResponse({'error': 'Invalid authentication token'}, status=400)


def confirm_order(request):
    return render(request)


def cancel_order(request):
    return render(request)


def pay_order(request):
    return render(request)

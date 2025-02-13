import json
from json.decoder import JSONDecodeError

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from games.models import Game
from games.serializers import GameSerializer
from shared import utils
from shared.decorators import get_required, post_required

from . import utils as order_utils
from .models import Order
from .serializers import OrderSerializer


@csrf_exempt
@post_required
def add_order(request) -> str:
    """Crea un pedido vacío."""
    token = utils.extract_token(request.headers.get('Authorization'))
    if not token:
        return JsonResponse({'error': 'Invalid authentication token'}, status=400)

    user = utils.get_authenticated_user(token)
    if not user:
        return JsonResponse({'error': 'Unregistered authentication token'}, status=401)

    order = Order.objects.create(user=user)
    return JsonResponse({'id': order.pk}, status=200)


@get_required
def order_detail(request, order_pk: int) -> str:
    """Lista los detalles de un pedido, buscado por su clave primaria."""
    token = utils.extract_token(request.headers.get('Authorization'))
    if not token:
        return JsonResponse({'error': 'Invalid authentication token'}, status=400)

    user = utils.get_authenticated_user(token)
    if not user:
        return JsonResponse({'error': 'Unregistered authentication token'}, status=401)

    try:
        order = Order.objects.get(pk=order_pk)
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)

    if user != order.user:
        return JsonResponse({'error': 'User is not the owner of requested order'}, status=403)

    serializer = OrderSerializer(order, request=request)
    return serializer.json_response()


@get_required
def order_game_list(request, order_pk: int) -> str:
    """Lista todos los juegos almacenados en un pedido, buscado por su clave primaria."""
    token = utils.extract_token(request.headers.get('Authorization'))
    if not token:
        return JsonResponse({'error': 'Invalid authentication token'}, status=400)

    user = utils.get_authenticated_user(token)
    if not user:
        return JsonResponse({'error': 'Unregistered authentication token'}, status=401)

    try:
        order = Order.objects.get(pk=order_pk)
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)

    if user != order.user:
        return JsonResponse({'error': 'User is not the owner of requested order'}, status=403)

    games = order.games.all()
    serializer = GameSerializer(games, request=request)
    return serializer.json_response()


@csrf_exempt
@post_required
def add_game_to_order(request, order_pk: int) -> str:
    """Añade un juego a un pedido, buscado por su clave primaria."""
    try:
        data = json.loads(request.body)
    except JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)

    if not utils.validate_required_fields(data, ['game-slug']):
        return JsonResponse({'error': 'Missing required fields'}, status=400)

    token = utils.extract_token(request.headers.get('Authorization'))
    if not token:
        return JsonResponse({'error': 'Invalid authentication token'}, status=400)

    user = utils.get_authenticated_user(token)
    if not user:
        return JsonResponse({'error': 'Unregistered authentication token'}, status=401)

    try:
        order = Order.objects.get(pk=order_pk)
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)

    try:
        game = Game.objects.get(slug=data['game-slug'])
    except Game.DoesNotExist:
        return JsonResponse({'error': 'Game not found'}, status=404)

    if user != order.user:
        return JsonResponse({'error': 'User is not the owner of requested order'}, status=403)

    game.rest_stock()
    order.games.add(game)
    return JsonResponse({'num-games-in-order': order.games.count()}, status=200)


@csrf_exempt
@post_required
def change_order_status(request, order_pk: int) -> str:
    """Cambia el estado de un pedido a cancelado o confirmado, buscado por su clave primaria."""
    try:
        data = json.loads(request.body)
    except JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)

    if not utils.validate_required_fields(data, ['status']):
        return JsonResponse({'error': 'Missing required fields'}, status=400)

    token = utils.extract_token(request.headers.get('Authorization'))
    if not token:
        return JsonResponse({'error': 'Invalid authentication token'}, status=400)

    user = utils.get_authenticated_user(token)
    if not user:
        return JsonResponse({'error': 'Unregistered authentication token'}, status=401)

    try:
        order = Order.objects.get(pk=order_pk)
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)

    if user != order.user:
        return JsonResponse({'error': 'User is not the owner of requested order'}, status=403)

    status = int(data['status'])
    if status not in [-1, 2]:
        return JsonResponse({'error': 'Invalid status'}, status=400)

    if order.get_status_display() != 'Initiated':
        return JsonResponse(
            {'error': 'Orders can only be confirmed/cancelled when initiated'}, status=400
        )

    if status == -1:
        for game in order.games.all():
            game.sum_stock()

    order.status = status
    order.save()
    return JsonResponse({'status': order.get_status_display()}, status=200)


@csrf_exempt
@post_required
def pay_order(request, order_pk: int) -> str:
    """Cambia el estado de un pedido a pagado, buscado por su clave primaria."""
    try:
        data = json.loads(request.body)
    except JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)

    if not utils.validate_required_fields(data, ['card-number', 'exp-date', 'cvc']):
        return JsonResponse({'error': 'Missing required fields'}, status=400)

    token = utils.extract_token(request.headers.get('Authorization'))
    if not token:
        return JsonResponse({'error': 'Invalid authentication token'}, status=400)

    user = utils.get_authenticated_user(token)
    if not user:
        return JsonResponse({'error': 'Unregistered authentication token'}, status=401)

    try:
        order = Order.objects.get(pk=order_pk)
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)

    if user != order.user:
        return JsonResponse({'error': 'User is not the owner of requested order'}, status=403)

    if order.get_status_display() != 'Confirmed':
        return JsonResponse({'error': 'Orders can only be paid when confirmed'}, status=400)

    error = order_utils.validate_card_details(data['card-number'], data['exp-date'], data['cvc'])
    if error:
        return JsonResponse({'error': error}, status=400)

    order.status = 3
    order.save()
    return JsonResponse({'status': order.get_status_display(), 'key': order.key}, status=200)

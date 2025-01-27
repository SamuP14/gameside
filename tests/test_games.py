import json

import pytest
from django.contrib.auth.models import User
from model_bakery import baker

from categories.models import Category
from games.models import Game, Review
from platforms.models import Platform

from .helpers import compare_games, compare_reviews

# ==============================================================================
# GAMES
# ==============================================================================


@pytest.mark.django_db
def test_game_list(client):
    for game in (games := baker.make(Game, _fill_optional=True, _quantity=10)):
        game.platforms.set(baker.make(Platform, _fill_optional=True, _quantity=3))
    response = client.get('/api/games/')
    assert response.status_code == 200
    response_body = json.loads(response.content)
    for rgame, egame in zip(response_body, games):
        compare_games(rgame, egame)


@pytest.mark.django_db
def test_game_list_fails_when_method_is_not_allowed(client):
    response = client.post('/api/games/')
    assert response.status_code == 405


@pytest.mark.django_db
def test_game_list_with_querystring_filter(client):
    test_category = baker.make(Category, slug='category-slug', _fill_optional=True)
    test_platform = baker.make(Platform, slug='platform-slug', _fill_optional=True)
    games = baker.make(Game, category=test_category, _fill_optional=True, _quantity=10)
    for game in games:
        game.platforms.add(test_platform)
        game.platforms.add(baker.make(Platform, _fill_optional=True))
    response = client.get('/api/games/?category=category-test&platform=platform-test')
    assert response.status_code == 200
    response_body = json.loads(response.content)
    for rgame, egame in zip(response_body, games):
        compare_games(rgame, egame)


@pytest.mark.django_db
def test_game_list_with_querystring_filter_fails_when_method_is_not_allowed(client):
    response = client.post('/api/games/?category=category-test&platform=platform-test')
    assert response.status_code == 405


@pytest.mark.django_db
def test_game_detail(client):
    game = baker.make(Game, _fill_optional=True)
    response = client.get(f'/api/games/{game.slug}/')
    assert response.status_code == 200
    rgame = json.loads(response.content)
    compare_games(rgame, game)


@pytest.mark.django_db
def test_game_detail_fails_when_method_is_not_allowed(client):
    response = client.post('/api/games/test/')
    assert response.status_code == 405


@pytest.mark.django_db
def test_game_detail_fails_when_game_does_not_exist(client):
    response = client.get('/api/games/test/')
    assert response.status_code == 404
    response_body = json.loads(response.content)
    assert response_body['error'] == 'Game not found'


# ==============================================================================
# REVIEWS
# ==============================================================================


@pytest.mark.django_db
def test_review_list(client):
    game = baker.make(Game, _fill_optional=True)
    reviews = baker.make(Review, game=game, _fill_optional=True, _quantity=10)
    response = client.get(f'/api/games/{game.slug}/reviews/')
    assert response.status_code == 200
    response_body = json.loads(response.content)
    for rreview, ereview in zip(response_body, reviews):
        compare_reviews(rreview, ereview)


@pytest.mark.django_db
def test_review_list_fails_when_method_is_not_allowed(client):
    response = client.post('/api/games/test/reviews/')
    assert response.status_code == 405


@pytest.mark.django_db
def test_review_detail(client):
    game = baker.make(Game, _fill_optional=True)
    review = baker.make(Review, game=game, _fill_optional=True)
    response = client.get(f'/api/games/reviews/{review.pk}/')
    assert response.status_code == 200
    rreview = json.loads(response.content)
    compare_reviews(rreview, review)


@pytest.mark.django_db
def test_review_detail_fails_when_method_is_not_allowed(client):
    response = client.post('/api/games/reviews/1/')
    assert response.status_code == 405


@pytest.mark.django_db
def test_add_review(client):
    user = baker.make(User, _fill_optional=True)
    token = baker.make('users.Token', user=user)
    game = baker.make(Game, _fill_optional=True)
    data = {
        'token': str(token.key),
        'rating': 5,
        'comment': 'This is a test comment',
    }
    response = client.post(
        f'/api/games/{game.slug}/reviews/add/', json.dumps(data), content_type='application/json'
    )
    assert response.status_code == 200
    ereview = Review.objects.get(game=game)
    assert ereview.rating == data['rating']
    assert ereview.comment == data['comment']
    assert ereview.game == game
    assert ereview.author == user

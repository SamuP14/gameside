import pytest
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

from categories.models import Category
from games.models import Game, Review
from orders.models import Order
from platforms.models import Platform
from users.models import Token


@pytest.mark.django_db
def test_required_apps_are_installed():
    PROPER_APPS = ('shared', 'games', 'platforms', 'categories', 'orders', 'users')

    custom_apps = [app for app in settings.INSTALLED_APPS if not app.startswith('django')]
    for app in PROPER_APPS:
        app_config = f'{app}.apps.{app.title()}Config'
        assert app_config in custom_apps, (
            f'La aplicación <{app}> no está "creada/instalada" en el proyecto.'
        )
    assert len(custom_apps) >= len(PROPER_APPS), (
        'El número de aplicaciones propias definidas en el proyecto no es correcto.'
    )


@pytest.mark.django_db
def test_game_model_has_proper_fields():
    PROPER_FIELDS = (
        'title',
        'slug',
        'description',
        'cover',
        'price',
        'stock',
        'released_at',
        'pegi',
        'category',
        'platforms',
    )
    for field in PROPER_FIELDS:
        assert getattr(Game, field) is not None, f'El campo <{field}> no está en el modelo Subject.'


@pytest.mark.django_db
def test_review_model_has_proper_fields():
    PROPER_FIELDS = ('rating', 'comment', 'game', 'author', 'created_at', 'updated_at')
    for field in PROPER_FIELDS:
        assert getattr(Review, field) is not None, (
            f'El campo <{field}> no está en el modelo Lesson.'
        )


@pytest.mark.django_db
def test_category_model_has_proper_fields():
    PROPER_FIELDS = ('name', 'slug', 'description', 'color')
    for field in PROPER_FIELDS:
        assert getattr(Category, field) is not None, (
            f'El campo <{field}> no está en el modelo Enrollment.'
        )


@pytest.mark.django_db
def test_platform_model_has_proper_fields():
    PROPER_FIELDS = ('name', 'slug', 'description', 'logo')
    for field in PROPER_FIELDS:
        assert getattr(Platform, field) is not None, (
            f'El campo <{field}> no está en el modelo Profile.'
        )


@pytest.mark.django_db
def test_order_model_has_proper_fields():
    PROPER_FIELDS = ('status', 'key', 'user', 'games', 'created_at', 'updated_at')
    for field in PROPER_FIELDS:
        assert getattr(Order, field) is not None, (
            f'El campo <{field}> no está en el modelo Profile.'
        )


@pytest.mark.django_db
def test_token_model_has_proper_fields():
    PROPER_FIELDS = ('user', 'key', 'created_at')
    for field in PROPER_FIELDS:
        assert getattr(Token, field) is not None, (
            f'El campo <{field}> no está en el modelo Profile.'
        )


@pytest.mark.django_db
def test_review_model_has_proper_validators():
    validators = Review.rating.field.validators
    assert len(validators) == 2, (
        'Debe haber dos validadores (min y max) para el campo "mark" de Enrollment.'
    )
    if 'less' in validators[0].message:
        max_validator = validators[0]
        min_validator = validators[1]
    else:
        min_validator = validators[0]
        max_validator = validators[1]
    assert isinstance(min_validator, MinValueValidator)
    assert isinstance(max_validator, MaxValueValidator)
    assert min_validator.limit_value == 1
    assert max_validator.limit_value == 5


@pytest.mark.django_db
def test_models_are_available_on_admin(admin_client):
    MODELS = (
        'games.Game',
        'games.Review',
        'categories.Category',
        'platforms.Platform',
        'orders.Order',
        'users.Token',
    )

    for model in MODELS:
        url_model_path = model.replace('.', '/').lower()
        url = f'/admin/{url_model_path}/'
        response = admin_client.get(url)
        assert response.status_code == 200, f'El modelo <{model}> no está habilitado en el admin.'

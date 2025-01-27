import json

import pytest
from model_bakery import baker

from categories.models import Category

from .helpers import compare_categories


@pytest.mark.django_db
def test_category_list(client):
    categories = baker.make(Category, _fill_optional=True, _quantity=10)
    response = client.get('/api/categories/')
    assert response.status_code == 200
    response_body = json.loads(response.content)
    for rcategory, ecategory in zip(response_body, categories):
        compare_categories(rcategory, ecategory)


@pytest.mark.django_db
def test_category_list_fails_when_method_is_not_allowed(client):
    response = client.post('/api/categories/')
    assert response.status_code == 405


@pytest.mark.django_db
def test_category_detail(client):
    category = baker.make(Category, _fill_optional=True)
    response = client.get(f'/api/categories/{category.slug}/')
    assert response.status_code == 200
    rcategory = json.loads(response.content)
    compare_categories(rcategory, category)


@pytest.mark.django_db
def test_category_detail_fails_when_method_is_not_allowed(client):
    response = client.post('/api/categories/test/')
    assert response.status_code == 405


@pytest.mark.django_db
def test_category_detail_fails_when_category_does_not_exist(client):
    response = client.get('/api/categories/test/')
    assert response.status_code == 404
    response_body = json.loads(response.content)
    assert response_body['error'] == 'Category not found'

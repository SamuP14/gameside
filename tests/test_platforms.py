import json

import pytest
from model_bakery import baker

from platforms.models import Platform

from .helpers import compare_platforms


@pytest.mark.django_db
def test_platform_list(client):
    platforms = baker.make(Platform, _fill_optional=True, _quantity=10)
    response = client.get('/api/platforms/')
    assert response.status_code == 200
    response_body = json.loads(response.content)
    for rplatform, eplatform in zip(response_body, platforms):
        compare_platforms(rplatform, eplatform)


@pytest.mark.django_db
def test_platform_list_fails_when_method_is_not_allowed(client):
    response = client.post('/api/platforms/')
    assert response.status_code == 405


@pytest.mark.django_db
def test_platform_detail(client):
    platform = baker.make(Platform, _fill_optional=True)
    response = client.get(f'/api/platforms/{platform.slug}/')
    assert response.status_code == 200
    rplatform = json.loads(response.content)
    compare_platforms(rplatform, platform)


@pytest.mark.django_db
def test_platform_detail_fails_when_method_is_not_allowed(client):
    response = client.post('/api/platforms/test/')
    assert response.status_code == 405


@pytest.mark.django_db
def test_platform_detail_fails_when_platform_does_not_exist(client):
    response = client.get('/api/platforms/test/')
    assert response.status_code == 404
    response_body = json.loads(response.content)
    assert response_body['error'] == 'Platform not found'

import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from users.models import UserAccount
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()



# @pytest.mark.django_db
# @pytest.mark.override_settings(DATABASE_ROUTERS=[])
# @pytest.fixture

# Test happy path for user-register

@pytest.mark.django_db(databases=['default', 'users'])
def test_register_regular_user_success(api_client):
    #ARRANGE
    url = reverse('user-register')
    _data = {
        'name': 'Test User',
        'email': 'test_user@gmail.com',
        'password': 'user_password',
        're_password': 'user_password',
        'is_realtor': 'False'
    }

    #ACT

    response = api_client.post(url, data=_data,format='json')

    #ASSERT

    assert response.status_code == status.HTTP_201_CREATED
    assert 'success' in response.data
    assert response.data['success'] == 'User created successfully'
    assert 'email' in response.data
    assert User.objects.filter(email= 'test_user@gmail.com').exists()
    user = User.objects.get(email= 'test_user@gmail.com')
    assert user.is_realtor is False

    return None


@pytest.mark.django_db(databases=['default', 'users'])
def test_register_realtor_user_success(api_client):

    #ARRANGE
    url = reverse('user-register')
    _data = {
        'name': 'Test Realtor',
        'email': 'test_realtor@gmail.com',
        'password': 'realtor_password',
        're_password': 'realtor_password',
        'is_realtor': 'True'
    }

    #ACT

    response = api_client.post(url, data=_data,format='json')

    #ASSERT

    assert response.status_code == status.HTTP_201_CREATED
    assert 'success' in response.data
    assert response.data['success'] == 'Realtor created successfully'

    # assert 'email' in response.data
    assert User.objects.filter(email= 'test_realtor@gmail.com').exists()
    user = User.objects.get(email= 'test_realtor@gmail.com')
    assert user.is_realtor is True

    return None

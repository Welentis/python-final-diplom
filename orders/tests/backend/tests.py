import yaml
import pytest
import json
from django.urls import reverse
from backend.models import *
from django.test import Client
from django.contrib.auth.hashers import make_password
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestView:
    @pytest.fixture
    def test_password(self):
        return 'str0ngp@ssw0rd'

    @pytest.fixture
    def user_shop(self, test_password):
        user = User.objects.create(
            email="testuser2@example.com",
            password=make_password(test_password),
            first_name="John2",
            last_name="Doe2",
            username="testuser2",
            type="shop",
            company="Company2",
            position="Developer2"
        )
        return user

    @pytest.fixture
    def user_buyer(self, test_password):
        user = User.objects.create(
            email="testuser3@example.com",
            password=make_password(test_password),
            first_name="John3",
            last_name="Doe3",
            username="testuser3",
            type="buyer",
            company="Company3",
            position="Developer3"
        )
        return user

    @pytest.fixture
    def user_data(self, test_password):
        return {"email": "testuser1@example.com",
                "password": 'password1',
                "first_name": "John1",
                "last_name": "Doe1",
                "username": "testuser1",
                "type": "shop",
                "company": "Company1",
                "position": "Developer1"}

    @pytest.fixture
    def client(self):
        return Client()

    def test_user_registration(self, user_data, client):
        url = reverse('register')
        response = client.post(url, data=json.dumps(user_data), content_type='application/json')
        assert response.status_code == 200
        user = User.objects.get(username=user_data['username'])
        assert user is not None
        assert user.email == user_data['email']

    def test_user_registration_duplicate(self, user_data, client):
        url = reverse('register')
        response = client.post(url, data=json.dumps(user_data), content_type='application/json')
        assert response.status_code == 200
        # проверка попытки зарегистрировать дубликат пользователя
        response = client.post(url, data=json.dumps(user_data), content_type='application/json')
        assert response.status_code == 400

    def test_user_login_success(self, user_shop, client, test_password):
        url = reverse('login')
        data = {
            'username': user_shop.username,
            'password': test_password,
        }
        response = client.post(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 200
        assert response.json()['status'] == True
        assert response.json()['you are now logged in as'] == user_shop.username

    def test_user_login_invalid_credentials(self, client):
        url = reverse('login')
        data = {
            'username': 'nouser',
            'password': 'nopassword',
        }
        response = client.post(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 200
        assert response.json()['status'] == 'invalid data'

    @pytest.fixture
    def token_shop(self, user_shop):
        token, created = Token.objects.get_or_create(user=user_shop)
        return token

    # Фикстура для APIClient с аутентификацией
    @pytest.fixture
    def auth_client_shop(self, token_shop):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token_shop.key)
        return client

    @pytest.fixture
    def token_buyer(self, user_buyer):
        token, created = Token.objects.get_or_create(user=user_buyer)
        return token

    # Фикстура для APIClient с аутентификацией
    @pytest.fixture
    def auth_client_buyer(self, token_buyer):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token_buyer.key)
        return client

    def test_partner_update(self, user_shop, auth_client_shop):
        data = {
            "shop": 'Test shop',
            "categories": [{"id": 1, "name": "Category 1"}, {"id": 2, "name": "Category 2"}],
            "goods": [
                {
                    "name": "Product 1",
                    "category": 1,
                    "model": "Product 1 model",
                    "price": 1000,
                    "price_rrc": 1200,
                    "quantity": 7000,
                    "parameters": {
                        "color": "black",
                        "size": "XL"
                    }
                },
            ]
        }
        url = reverse('update_products', kwargs={'file_name': 'test.yaml'})
        with open('../data/test.yaml', 'w', encoding='UTF-8') as f:
            yaml.dump(data, f)
        response = auth_client_shop.post(url)
        assert response.json()['Code'] == 201
        assert response.json()['Status'] == True

    def test_get_products(self, user_buyer, auth_client_buyer):
        url = reverse('products')
        response = auth_client_buyer.get(url)
        assert response.status_code == 200

    def test_get_products_detail(self, user_buyer, auth_client_buyer):
        url = reverse('products', kwargs={'id': 1})
        response = auth_client_buyer.get(url)
        assert response.status_code == 200

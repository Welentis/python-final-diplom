# import pytest
# from rest_framework.test import APIClient
# from backend.models import *
#
#
# @pytest.fixture
# def client():
#     return APIClient()
#
#
# @pytest.fixture
# def user_admin():
#     return User.objects.create_user('admin')
#
#
# @pytest.fixture
# def user():
#     return User.objects.create_user(first_name='test2',
#                                     last_name='test2',
#                                     email='test2@test.com',
#                                     password='test2',
#                                     username='test2',
#                                     type='buyer'
#                                     )
#
# #
# @pytest.fixture
# def user_shop():
#     return User.objects.create_user(first_name='test4',
#                                     last_name='test4',
#                                     email='test4@test.com',
#                                     password='test4',
#                                     type='shop',
#                                     username='test4'
#                                     )
#
# @pytest.mark.django_db
# def test_register(client):
#     response = client.post(f'/api/register', data={'first_name': 'test1',
#                                                    'last_name': 'test1',
#                                                    'email': 'test1@test.com',
#                                                    'password': 'test1',
#                                                    'username': 'test1',
#                                                    'type': 'shop',
#                                                    'company': '',
#                                                    'position': '',
#                                                    }
#                            )
#     assert response.status_code == 201
#
#
# @pytest.mark.django_db
# def test_login(client):
#     response = client.post(f'/api/login',
#                            data={'password': 'test1',
#                                  'username': 'test1'
#                                  }
#                            )
#     assert response.status_code == 201
#
#
# @pytest.mark.django_db
# def test_update_shop_products(client, user_admin):
#     token, creation = Token.objects.get_or_create(user=user_admin)
#     response = client.post(f'/api/update/shop1.yaml', HTTP_AUTHORIZATION=f'Token {token}')
#     assert response.status_code == 201
#
#
# @pytest.mark.django_db
# def test_register(client):
#     response = client.post(f'/api/register', data={'first_name': 'test3',
#                                                    'last_name': 'test3',
#                                                    'email': 'test3@test.com',
#                                                    'password': 'test3',
#                                                    'username': 'test3',
#                                                    'type': 'buyer',
#                                                    'company': '',
#                                                    'position': '',
#                                                    }
#                            )
#     assert response.status_code == 201
#
#
# @pytest.mark.django_db
# def test_get_all_products(client, user):
#     token, creation = Token.objects.get_or_create(user=user)
#     response = client.get(f'/api/products', HTTP_AUTHORIZATION=f'Token {token}')
#     assert response.status_code == 201
#
#
# @pytest.mark.django_db
# def test_get_product_info(client, user, user_shop):
#     token, creation = Token.objects.get_or_create(user=user)
#     response = client.get(f'/api/products/1', HTTP_AUTHORIZATION=f'Token {token}')
#     assert response.status_code == 201
#
#
# @pytest.mark.django_db
# def test_get_basket(client, user, user_shop):
#     token, creation = Token.objects.get_or_create(user=user)
#     new_order = Order.objects.create(user=user,
#                                      state='basket'
#                                      )
#     OrderItem.objects.create(order=new_order,
#                              product=Product.objects.get(id=1),
#                              shop=Shop.objects.get(user=user.id),
#                              quantity=3,
#                              )
#     # Act
#     response = client.get(f'user/basket',
#                           data={'user': user.id}
#                           )
#     # Assert
#     assert response.status_code == 200
#     data = response.json()
#     assert data[0]['Список товаров: '][0].name == 'Смартфон Apple iPhone XS Max 512GB (золотистый)'
#     assert data[0]['Итог: ']['Сумма: '] > 110100


import pytest
import json
from django.urls import reverse
from backend.models import *
from django.test import Client
from django.contrib.auth.hashers import make_password


@pytest.mark.django_db
class TestUserRegisterView:
    @pytest.fixture
    def test_password(self):
        return 'str0ngp@ssw0rd'

    @pytest.fixture
    def test_user(self, test_password):
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

    def test_user_login_success(self, test_user, client, test_password):
        url = reverse('login')
        data = {
            'username': test_user.username,
            'password': test_password,
        }
        response = client.post(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 200
        assert response.json()['status'] == True
        assert response.json()['you are now logged in as'] == test_user.username

    def test_user_login_invalid_credentials(self, client):
        url = reverse('login')
        data = {
            'username': 'nouser',
            'password': 'nopassword',
        }
        response = client.post(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 200
        assert response.json()['status'] == 'invalid data'


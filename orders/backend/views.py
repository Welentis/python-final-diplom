from django.db import IntegrityError
from rest_framework import status
import yaml
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import *
from .signals import new_user_registered, new_order
from drf_spectacular.views import SpectacularAPIView
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


# Create your views here.

class PartnerUpdate(SpectacularAPIView, APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    throttle_classes = [UserRateThrottle]

    def post(self, request, file_name):
        if request.user.type == 'shop':
            import os
            print(os.getcwd())
            with open(f'../data/{file_name}', 'r', encoding='UTF-8') as file:
                data = yaml.safe_load(file)

                shop, _ = Shop.objects.get_or_create(name=data['shop'], creater=request.user)

                for category in data['categories']:
                    category_object, _ = Category.objects.get_or_create(id=category['id'], name=category['name'])
                    category_object.shops.add(shop.id)
                    category_object.save()

                for item in data['goods']:
                    product, _ = Product.objects.get_or_create(name=item['name'], category_id=item['category'])

                    product_info, _ = ProductInfo.objects.get_or_create(product_id=product.id,
                                                                        shop=shop,
                                                                        name=item['model'],
                                                                        price=item['price'],
                                                                        price_rrc=item['price_rrc'],
                                                                        quantity=item['quantity'],
                                                                        )
                    for name, value in item['parameters'].items():
                        parameter_object, _ = Parameter.objects.get_or_create(name=name)
                        ProductParameter.objects.get_or_create(product_info_id=product_info.id,
                                                               parameter_id=parameter_object.id,
                                                               value=value)

            return JsonResponse({'Status': True, 'Code': 201})
        else:
            return JsonResponse({'Status': False, 'error': 403, 'описание:': 'недостаточно прав'})


class UserRegisterView(SpectacularAPIView, APIView):
    throttle_classes = [AnonRateThrottle]

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.create(
                email=request.data['email'],
                password=request.data['password'],
                first_name=request.data['first_name'],
                last_name=request.data['last_name'],
                username=request.data['username'],
                type=request.data['type'],
                company=request.data['company'],
                position=request.data['position']
            )
            user.set_password(request.data['password'])
            user.save()
            new_user_registered.send(sender=self.__class__, user_id=user.id)
            return JsonResponse({'Status': True})
        except IntegrityError:
            return Response("Username already in use", status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(SpectacularAPIView, APIView):
    throttle_classes = [AnonRateThrottle]

    def post(self, request, *args, **kwargs):
        user = authenticate(
            request,
            username=request.data['username'],
            password=request.data['password']
        )
        if user is not None:
            if user.is_active:
                login(request, user)
                return JsonResponse({
                    'status': True,
                    'you are now logged in as': request.user.username
                })
        else:
            return JsonResponse({'status': 'invalid data'})


class ProductView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    throttle_classes = [UserRateThrottle]

    def get(self, request, *args, **kwargs):
        quareset = Product.objects.select_related('category').all()
        serializer = ProductSerializer(quareset, many=True)
        return Response(serializer.data)


class ProductDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    throttle_classes = [UserRateThrottle]

    def get(self, request, id, *args, **kwargs):
        queryset = Product.objects.filter(id=id)
        serializer_class = ProductSerializer(queryset, many=True)
        return Response(serializer_class.data, )


class OrderView(SpectacularAPIView, APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    throttle_classes = [UserRateThrottle]

    def get(self, request, *args, **qwargs):
        queryset = Order.objects.filter(user_id=request.user.id)
        serializer_class = OrderSerializer(queryset, many=True)
        return Response(serializer_class.data)

    def post(self, request, *args, **qwargs):
        if 'product' in request.data and 'shop' in request.data and 'quantity' in request.data:
            try:
                product = Product.objects.get(id=request.data['product'])
                shop = Shop.objects.get(id=request.data['shop'])
                info = ProductInfo.objects.get(product_id=request.data['product'])
                qs_category = Category.objects.filter(id=product.category_id)
                serializer_class = CategorySerializer(qs_category, many=True)
                if int(serializer_class.data[0]['shops'][0]['id']) == int(request.data['shop']):
                    if info.quantity >= int(request.data['quantity']):
                        order, _ = Order.objects.get_or_create(user_id=request.user.id, state='new')
                        OrderItem.objects.filter(order=order, product=product, shop=shop).update(
                            quantity=request.data['quantity'])
                        order_item, _ = OrderItem.objects.get_or_create(order=order, product=product, shop=shop,
                                                                        quantity=request.data['quantity'])
                        new_order.send(sender=self.__class__, user_id=request.user.id)
                        return Response({'Status': True, 'Code': 201, 'id': order_item.id})
                    else:
                        return Response({'Status': False, 'Error': 400,
                                         'описание': 'Количество товаров в карзине выше, чем имеется'})
                else:
                    return Response(
                        {'Status': False, 'Error': 400, 'описание': 'Данный товар принадлежит другому магазину'})
            except Shop.DoesNotExist:
                return Response({'Status': False, 'Error': 400, 'описание': 'Неверный id магазинa'})
            except Product.DoesNotExist:
                return Response({'Status': False, 'Error': 400, 'описание': 'Неверный id товара'})
        else:
            return Response({'Status': False, 'Error': 400, 'описание': 'Переданы не все параметры'})


class OrderConfirmationView(SpectacularAPIView, APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    throttle_classes = [UserRateThrottle]

    def post(self, request, *args, **kwargs):
        order = Order.objects.get(user_id=request.user.id, state='new')
        action = request.data['action']
        if action == 'approve':
            order.state = 'confirmed'
            order.save()
            return JsonResponse({'Status': True})
        elif action == 'disapprove':
            return JsonResponse({'Status': 'Now you can change your order'})

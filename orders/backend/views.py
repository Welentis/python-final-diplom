import yaml
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .serializers import *


# Create your views here.

class PartnerUpdate(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, file_name):
        if request.user.type == 'shop':
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


class UserRegisterView(APIView):
    def post(self, request, *args, **kwargs):
        user = User.objects.create(
            email=request.data['email'],
            password=request.data['password'],
            username=request.data['username'],
            type=request.data['type'],
            company=request.data['company'],
            position=request.data['position']
        )
        user.set_password(request.data['password'])
        user.save()
        return JsonResponse({'Status': True})


class UserLoginView(APIView):
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
    # queryset = Product.objects.select_related('category').all()
    # serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    #
    def get(self, request, *args, **kwargs):
        quareset = Product.objects.select_related('category').all()
        serializer = ProductSerializer(quareset, many=True)
        # permission_classes = [IsAuthenticated]
        return Response(serializer.data)
    #     queryset = Product.objects.select_related('category').all()
    #     serializer_class = ProductSerializer
    #     permission_classes = [IsAuthenticated]
    #     return Response(serializer_class.data)


class ProductDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id, *args, **kwargs):
        queryset = Product.objects.filter(id=id)
        serializer_class = ProductSerializer(queryset, many=True)
        return Response(serializer_class.data, )

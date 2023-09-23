from rest_framework.relations import StringRelatedField
from rest_framework.serializers import ModelSerializer

from .models import *


# class ProductSerializer(ModelSerializer):
#     category = StringRelatedField()
#
#     class Meta:
#         model = Product
#         fields = ('name', 'category',)
#         read_only_fields = ['id']
class ProductParameterSerializer(ModelSerializer):
    parameter = StringRelatedField()

    class Meta:
        model = ProductParameter
        fields = ('parameter', 'value')


class ShopSerializer(ModelSerializer):
    class Meta:
        model = Shop
        fields = ('id', 'name', 'creater')


class CategorySerializer(ModelSerializer):
    shops = ShopSerializer(many=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'shops')


class ProductInfoSerializer(ModelSerializer):
    product_parameters = ProductParameterSerializer(many=True)

    class Meta:
        model = ProductInfo
        fields = ('quantity', 'price', 'price_rrc', 'product_parameters')


class ProductSerializer(ModelSerializer):
    category = CategorySerializer()
    product_infos = ProductInfoSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'product_infos', 'category')

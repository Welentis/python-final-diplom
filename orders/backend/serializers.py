from rest_framework.relations import StringRelatedField
from rest_framework.serializers import ModelSerializer, IntegerField

from .models import *


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name']
        read_only_fields = ['id']


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


# class ContactSerializer(ModelSerializer):
#     class Meta:
#         model = Contact
#         fields = ['value']
#
#
# class DetailedOrderItemSerializer(ModelSerializer):
#     product_info = ProductInfoSerializer(read_only=True)
#
#     class Meta:
#         model = OrderItem
#         fields = ['order', 'product_info', 'quantity']
#
#
# class OrderSerializer(ModelSerializer):
#     total_sum = IntegerField()
#     contact = ContactSerializer(read_only=True)
#
#     class Meta:
#         model = Order
#         fields = ['id', 'user', 'dt', 'state', 'total_sum', 'contact']
#         read_only_fields = ['id']
#         extra_kwargs = {
#             'user': {'write_only': True}
#         }
#
#
# class OrderInfoSerializer(ModelSerializer):
#     total_sum = IntegerField()
#     contact = ContactSerializer(read_only=True)
#     order_items = DetailedOrderItemSerializer(read_only=True, many=True)
#     user = UserSerializer(read_only=True)
#
#     class Meta:
#         model = Order
#         fields = ['dt', 'state', 'user', 'contact', 'order_items', 'total_sum']


class OrderItemsSerializer(ModelSerializer):
    product = ProductSerializer()
    shop = ShopSerializer()

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'shop', 'quantity',)


class OrderSerializer(ModelSerializer):
    ordered_items = OrderItemsSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'user_id', 'dt', 'state', 'ordered_items')

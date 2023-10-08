import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from .models import Product
from .serializers import ProductSerializer


# initialize the APIClient app
client = Client()


class GetAllProductsTest(TestCase):

    def test_get_all_products(self):
        # get API response
        response = client.get(reverse('products'))
        # get data from db
        product = Product.objects.all()
        serializer = ProductSerializer(product, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

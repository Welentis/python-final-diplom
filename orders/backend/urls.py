from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token
from .views import *


urlpatterns = [
    path('update/<str:file_name>', PartnerUpdate.as_view(), name='update_products'),
    path('register', UserRegisterView.as_view(), name='register'),
    path('login', UserLoginView.as_view(), name='login'),
    path('products', ProductView.as_view(), name='products'),
    path('products/<int:id>', ProductDetailView.as_view(), name='products'),
    path('order', OrderView.as_view(), name='order'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

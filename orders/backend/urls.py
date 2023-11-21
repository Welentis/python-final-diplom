from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('update/<str:file_name>', PartnerUpdate.as_view(), name='update_products'),
    path('register', UserRegisterView.as_view(), name='register'),
    path('login', UserLoginView.as_view(), name='login'),
    path('products', ProductView.as_view(), name='products'),
    path('products/<int:id>', ProductDetailView.as_view(), name='products'),
    path('order', OrderView.as_view(), name='order'),
    path('orderConfirm', OrderConfirmationView.as_view(), name='orderConfirm'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('social', include('social_django.urls'), name='social')

]

urlpatterns = format_suffix_patterns(urlpatterns)

from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    # path('contacts', ContactView.as_view(), name='contacts_view'),
    # path('contacts/<int:pk>/', views.ContactsDetail.as_view()),
    path('update/<str:file_name>', PartnerUpdate.as_view(), name='update_products'),
    # path('api-auth/', include('rest_framework.urls')),
    path('register', UserRegisterView.as_view(), name='register'),
    path('login', UserLoginView.as_view(), name='login'),
    # path('shops', ShopView.as_view(), name='shops'),
    path('products', ProductView.as_view(), name='products'),
    path('products/<int:id>', ProductDetailView.as_view(), name='products'),
    # path('basket', BasketView.as_view(), name='basket'),
    # path('order', OrderView.as_view(), name='order'),
    # path('categories', CategoryView.as_view(), name='categories'),

    # path('partner/update', PartnerUpdate.as_view(), name='partner-update'),
    # path('partner/state', PartnerState.as_view(), name='partner-state'),
    # path('partner/orders', PartnerOrders.as_view(), name='partner-orders'),
    # path('user/register', RegisterAccount.as_view(), name='user-register'),
    # path('user/register/confirm', ConfirmAccount.as_view(), name='user-register-confirm'),
    # path('user/details', AccountDetails.as_view(), name='user-details'),
    # path('user/login', LoginAccount.as_view(), name='user-login'),
    # path('user/password_reset', reset_password_request_token, name='password-reset'),
    # path('user/password_reset/confirm', reset_password_confirm, name='password-reset-confirm'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
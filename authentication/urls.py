from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from . import views

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # noqa: E501
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # noqa: E501

    path(
        'api/register/nutritionist/',
        views.RegisterNutritionistView.as_view(),
        name='register_nutritionist_api'
    ),
    path(
        'api/register/customer/',
        views.RegisterCustomerView.as_view(),
        name='register_customer_api'
    ),
]

urlpatterns += [
    path('login/', views.login, name='login'),
    path('register/nutritionist/', views.register_nutritionist, name='register_nutritionist'),  # noqa: E501
    path('register/customer/', views.register_customer, name='register_customer'),  # noqa: E501
]

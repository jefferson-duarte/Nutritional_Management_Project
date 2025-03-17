from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import api, site

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # noqa: E501
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # noqa: E501

    path(
        'api/register/nutritionist/',
        api.RegisterNutritionistView.as_view(),
        name='register_nutritionist_api'
    ),
    path(
        'api/register/customer/',
        api.RegisterCustomerView.as_view(),
        name='register_customer_api'
    ),
    path(
        'update_customer/<int:customer_id>/',
        api.UpdateCustomerView.as_view(),
        name='update_customer_api'
    ),
]

urlpatterns += [
    path('', site.home, name='home'),
    path('login/create/', site.login_create, name='login_create'),
    path('register/nutritionist/', site.register_nutritionist, name='register_nutritionist'),  # noqa: E501
    path('register/customer/', site.register_customer, name='register_customer'),  # noqa: E501
    path('update/customer/<int:customer_id>/', site.CustomerUpdateView.as_view(), name='update_customer'),  # noqa: E501
    path('additional-info/', site.additional_info, name='additional_info'),
]

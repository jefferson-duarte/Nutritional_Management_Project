from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from . import views

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # noqa: E501
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # noqa: E501
    path('login/', views.login, name='login'),
]

# urlpatterns += [
#     path('api/protected/', ProtectedView.as_view(), name='protected'),
# ]

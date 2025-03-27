from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('select-nutritionist/<int:nutritionist_id>/', views.select_nutritionist, name='select_nutritionist'),  # noqa:E501
]

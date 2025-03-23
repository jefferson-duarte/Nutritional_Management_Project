from django.urls import path

from . import views

urlpatterns = [
    path('plan_list', views.nutritional_plan_list, name='plan_list'),
    path('plan_create/<int:customer_id>', views.nutritional_plan_create, name='plan_create'),  # noqa:E501
    path('plan_edit/<int:pk>', views.nutritional_plan_edit, name='plan_edit'),
    path('plan_detail/<int:pk>', views.nutritional_plan_detail, name='plan_detail'),  # noqa:E501
    path('plan_delete/<int:pk>', views.nutritional_plan_delete, name='plan_delete'),  # noqa:E501
]

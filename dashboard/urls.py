from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('select-nutritionist/<int:nutritionist_id>/', views.select_nutritionist, name='select_nutritionist'),  # noqa:E501

    path('schedule/', views.schedule_appointment, name="schedule_appointment"),
    path('cancel/<int:appointment_id>/', views.cancel_appointment, name="cancel_appointment"),  # noqa:E501
    path('reschedule/<int:appointment_id>/', views.reschedule_appointment, name="reschedule_appointment"),  # noqa:E501
    path('delete_appointment/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'),  # noqa:E501
    path('confirm_delete_appointment/<int:appointment_id>/', views.confirm_delete_appointment, name='confirm_delete_appointment'),  # noqa:E501
]

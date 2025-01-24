from django.contrib import admin

from .models import CustomerProfile, NutritionistProfile


@admin.register(NutritionistProfile)
class NutritionistAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'registration_number', 'phone',
    ]


@admin.register(CustomerProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'phone',
    ]

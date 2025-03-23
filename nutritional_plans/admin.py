from django.contrib import admin

from .models import FoodItem, Meal, NutritionalPlan


@admin.register(NutritionalPlan)
class NutritionalAdmin(admin.ModelAdmin):
    list_display = ('title', 'nutritionist', 'client', 'created_at')
    list_filter = ('nutritionist', 'client', 'created_at')
    search_fields = ('title', 'description')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    raw_id_fields = ('nutritionist', 'client')
    prepopulated_fields = {'title': ('title',)}
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('title', 'description')
        }),
        ('Relations', {
            'fields': ('nutritionist', 'client')
        }),
        ('Date', {
            'fields': ('created_at',)
        })
    )


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('name', 'plan')
    list_filter = ('plan',)
    search_fields = ('name', 'description')
    raw_id_fields = ('plan',)
    fieldsets = (
        (None, {
            'fields': ('name', 'description')
        }),
        ('Relations', {
            'fields': ('plan',)
        })
    )


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'meal', 'quantity')
    list_filter = ('meal',)
    search_fields = ('name', 'quantity')
    raw_id_fields = ('meal',)
    fieldsets = (
        (None, {
            'fields': ('name', 'quantity')
        }),
        ('Relations', {
            'fields': ('meal',)
        })
    )

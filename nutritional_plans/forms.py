from django import forms

from .models import FoodItem, Meal, NutritionalPlan


class NutritionalPlanForm(forms.ModelForm):
    class Meta:
        model = NutritionalPlan
        fields = ['client', 'title', 'description']


class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['name', 'description']


class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['name', 'quantity']

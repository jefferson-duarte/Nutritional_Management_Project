from django import forms

from .models import FoodItem, Meal, NutritionalPlan


class NutritionalPlanForm(forms.ModelForm):
    class Meta:
        model = NutritionalPlan
        fields = ['client', 'title', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].widget.attrs['style'] = 'display:none;'
        self.fields['client'].label = ''


class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['name', 'description']


class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['name', 'quantity']

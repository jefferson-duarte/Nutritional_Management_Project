from django import forms

from .models import CustomerProfile


class CustomerAdditionalInfoForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = [
            'age',
            'gender',
            'height',
            'weight',
            'nutritional_goal',
            'diet_plan',
            'allergies',
            'last_appointment',
            'image',
        ]

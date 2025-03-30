from django import forms

from authentication.models import CustomerProfile, NutritionistProfile

from .models import Appointment


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["customer", "date", "notes"]
        widgets = {
            "date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user and user.is_authenticated:
            nutritionist_profile = NutritionistProfile.objects.filter(
                user=user).first()

            if nutritionist_profile:
                self.fields['customer'].queryset = CustomerProfile.objects.filter(  # noqa: E501
                    nutritionist=nutritionist_profile
                )

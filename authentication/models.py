from django.contrib.auth.models import User
from django.db import models


# Model for Nutritionist
class NutritionistProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    is_nutritionist = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


# Model for UserProfile
class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    nutritionist = models.ForeignKey(
        NutritionistProfile, on_delete=models.SET_NULL, null=True, blank=True
    )
    age = models.IntegerField(null=True, blank=True)
    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    nutritional_goal = models.CharField(max_length=100, null=True, blank=True)
    diet_plan = models.CharField(max_length=100, null=True, blank=True)
    allergies = models.CharField(max_length=200, null=True, blank=True)
    last_appointment = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)  # noqa:E501
    profile_complete = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

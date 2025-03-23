from django.contrib.auth.models import User
from django.db import models


class NutritionalPlan(models.Model):
    nutritionist = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='plans')
    client = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='client_plans')
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Meal(models.Model):
    plan = models.ForeignKey(
        NutritionalPlan, on_delete=models.CASCADE, related_name='meals')
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class FoodItem(models.Model):
    meal = models.ForeignKey(
        Meal, on_delete=models.CASCADE, related_name='food_items')
    name = models.CharField(max_length=255)
    quantity = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.quantity} of {self.name}"

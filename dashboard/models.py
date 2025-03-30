from django.db import models

from authentication.models import CustomerProfile, NutritionistProfile


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    nutritionist = models.ForeignKey(
        NutritionistProfile, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    date = models.DateTimeField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Appointment with {self.customer.user.username} on {self.date}"

from django.contrib.auth.models import User
from django.test import TestCase

from authentication.models import CustomerProfile, NutritionistProfile


class NutritionistProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='nutritionist', password='password')
        self.nutritionist_profile = NutritionistProfile.objects.create(
            user=self.user,
            registration_number='12345',
            phone='1234567890'
        )

    def test_str_method(self):
        self.assertEqual(str(self.nutritionist_profile), 'nutritionist')


class CustomerProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='customer', password='password')
        self.nutritionist_user = User.objects.create_user(
            username='nutritionist', password='password')
        self.nutritionist_profile = NutritionistProfile.objects.create(
            user=self.nutritionist_user,
            registration_number='12345',
            phone='1234567890'
        )
        self.customer_profile = CustomerProfile.objects.create(
            user=self.user,
            phone='1234567890',
            nutritionist=self.nutritionist_profile
        )

    def test_str_method(self):
        self.assertEqual(str(self.customer_profile), 'customer')

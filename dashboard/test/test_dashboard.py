from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from authentication.models import CustomerProfile, NutritionistProfile


class DashboardViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.nutritionist_user = User.objects.create_user(
            username='nutritionist', password='password')
        self.customer_user = User.objects.create_user(
            username='customer', password='password')
        self.nutritionist_profile = NutritionistProfile.objects.create(
            user=self.nutritionist_user,
            registration_number='12345',
            phone='1234567890'
        )
        self.customer_profile = CustomerProfile.objects.create(
            user=self.customer_user,
            phone='1234567890',
            nutritionist=self.nutritionist_profile
        )

    def test_dashboard_view_as_nutritionist(self):
        self.client.login(username='nutritionist', password='password')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'dashboard/nutritionist_dashboard.html')
        self.assertIn('customers', response.context)

    def test_dashboard_view_as_customer(self):
        self.client.login(username='customer', password='password')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/customer_dashboard.html')

    def test_dashboard_view_as_anonymous(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login_create'))

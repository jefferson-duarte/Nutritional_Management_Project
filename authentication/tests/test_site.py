from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from authentication.forms import CustomerAdditionalInfoForm
from authentication.models import CustomerProfile, NutritionistProfile


class HomeViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/home.html')


class LoginCreateViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('login_create')
        self.user_credentials = {
            'username': 'testuser',
            'password': 'password123'
        }
        self.user = User.objects.create_user(**self.user_credentials)

    def test_login_create_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/login.html')

    def test_login_create_view_post_invalid_credentials(self):
        response = self.client.post(self.url, {
            'username': 'wronguser',
            'password': 'wrongpassword'
        })
        self.assertRedirects(response, self.url)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Invalid credentials')


class RegisterCustomerViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('register_customer')

    def test_register_nutritionist_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'authentication/customer_registration.html')


class AdditionalInfoViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('additional_info')
        self.user_credentials = {
            'username': 'testuser',
            'password': 'password123'
        }
        self.user = User.objects.create_user(**self.user_credentials)
        self.client.login(**self.user_credentials)

    def test_additional_info_view_redirects_to_register_customer(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('register_customer'))

    def test_additional_info_view_redirects_to_dashboard_if_profile_complete(self):  # noqa: E501
        customer_profile = CustomerProfile.objects.create(  # noqa: F841
            user=self.user, profile_complete=True
        )
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('dashboard'))

    def test_additional_info_view_renders_form_if_profile_incomplete(self):
        customer_profile = CustomerProfile.objects.create(  # noqa: F841
            user=self.user, profile_complete=False
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'authentication/additional_info.html')
        self.assertIsInstance(
            response.context['form'], CustomerAdditionalInfoForm)

    def test_additional_info_view_post_valid_data(self):
        customer_profile = CustomerProfile.objects.create(
            user=self.user, profile_complete=False)
        form_data = {
            'address': '123 Main St',
            'phone_number': '1234567890'
        }
        response = self.client.post(self.url, form_data)
        self.assertRedirects(response, reverse('dashboard'))
        customer_profile.refresh_from_db()
        self.assertTrue(customer_profile.profile_complete)


class CustomerUpdateViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.nutritionist_credentials = {
            'username': 'nutritionist',
            'password': 'password123'
        }
        self.nutritionist = User.objects.create_user(
            **self.nutritionist_credentials)
        self.nutritionist_profile = NutritionistProfile.objects.create(
            user=self.nutritionist)
        self.customer_profile = CustomerProfile.objects.create(
            user=self.nutritionist,
            nutritionist=self.nutritionist_profile,
            profile_complete=False
        )
        self.url = reverse(
            'update_customer',
            kwargs={'customer_id': self.customer_profile.id}
        )
        self.client.login(**self.nutritionist_credentials)

    def test_customer_update_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'authentication/update_customer.html')
        self.assertEqual(response.context['customer'], self.customer_profile)

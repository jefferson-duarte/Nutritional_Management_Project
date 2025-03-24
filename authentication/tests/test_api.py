from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.test import APIRequestFactory, force_authenticate

from authentication.models import CustomerProfile, NutritionistProfile
from authentication.serializers import NutritionistProfileSerializer
from authentication.views.api import RegisterCustomerView, UpdateCustomerView


class RegisterCustomerViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = RegisterCustomerView.as_view()
        self.url = '/register/customer/'
        self.valid_payload = {
            'user': {
                'first_name': 'John',
                'last_name': 'Doe',
                'username': 'johndoe',
                'email': 'john@example.com',
                'password': 'securepassword123',
                'confirm_password': 'securepassword123'
            },
            'phone': '1234567890',
            'age': 30,
            'gender': 'M',
            'height': 1.75,
            'weight': 70,
            'nutritional_goal': 'Build muscle',
            'diet_plan': 'High protein',
            'allergies': 'None',
            'last_appointment': None
        }

    def test_register_customer_success(self):
        """Test successful customer registration"""
        request = self.factory.post(
            self.url, self.valid_payload, format='json')
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data['success'],
            'Customer registered successfully'
        )

        # Verify user was created
        user = User.objects.get(username='johndoe')
        self.assertEqual(user.email, 'john@example.com')

        # Verify customer profile was created
        customer_profile = CustomerProfile.objects.get(user=user)
        self.assertEqual(customer_profile.phone, '1234567890')

    def test_register_customer_missing_required_field(self):
        """Test registration with missing required field"""
        invalid_payload = self.valid_payload.copy()
        invalid_payload['user'].pop('username')

        request = self.factory.post(self.url, invalid_payload, format='json')
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('user', response.data)
        self.assertIn('username', response.data['user'])

    def test_register_customer_password_mismatch(self):
        """Test registration with password mismatch"""
        invalid_payload = self.valid_payload.copy()
        invalid_payload['user']['confirm_password'] = 'differentpassword'

        request = self.factory.post(self.url, invalid_payload, format='json')
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('user', response.data)
        self.assertIn('password', response.data['user'])

    def test_register_customer_duplicate_username(self):
        """Test registration with duplicate username"""
        # First create a user with the same username
        User.objects.create_user(
            username='johndoe',
            email='existing@example.com',
            password='testpass123'
        )

        request = self.factory.post(
            self.url, self.valid_payload, format='json')
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('user', response.data)
        self.assertIn('username', response.data['user'])

    def test_permission_classes(self):
        """Test that the view allows any user (unauthenticated)"""
        self.assertEqual(RegisterCustomerView.permission_classes, [AllowAny])


class RegisterNutritionistViewGetTest(TestCase):
    def setUp(self):
        self.url = reverse('register_nutritionist_api')

    def test_get_request_returns_form(self):
        """Test that GET request returns the registration form"""
        response = self.client.get(self.url)

        # Check response status code
        self.assertEqual(response.status_code, 200)

        # Check the correct template is used
        self.assertTemplateUsed(
            response, 'authentication/nutritionist_registration.html')

        # Check serializer is in context
        self.assertIn('form', response.context)
        self.assertIsInstance(
            response.context['form'], NutritionistProfileSerializer)

        # Check form fields are present in rendered content
        content = response.content.decode()
        self.assertIn('user[first_name]', content)
        self.assertIn('user[last_name]', content)
        self.assertIn('user[username]', content)
        self.assertIn('user[email]', content)
        self.assertIn('user[password]', content)
        self.assertIn('user[confirm_password]', content)
        self.assertIn('registration_number', content)
        self.assertIn('phone', content)

    def test_unauthenticated_access(self):
        """Test that unauthenticated users can access the registration page"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_authenticated_access(self):
        """Test that authenticated users can access the registration page"""
        User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class UpdateCustomerViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = UpdateCustomerView.as_view()
        self.nutritionist_user = User.objects.create_user(
            username='nutritionist',
            password='testpass123',
            email='nutritionist@example.com'
        )
        self.nutritionist = NutritionistProfile.objects.create(
            user=self.nutritionist_user,
            registration_number='12345',
            phone='1234567890'
        )

        self.other_nutritionist_user = User.objects.create_user(
            username='other_nutritionist',
            password='testpass123'
        )
        self.other_nutritionist = NutritionistProfile.objects.create(
            user=self.other_nutritionist_user,
            registration_number='54321',
            phone='0987654321'
        )

        self.customer = CustomerProfile.objects.create(
            user=User.objects.create_user(
                username='customer1',
                password='testpass123',
                email='customer1@example.com'
            ),
            nutritionist=self.nutritionist,
            phone='1111111111',
            age=25,
            gender='M'
        )

    def test_get_customer_not_found(self):
        """Test GET request for non-existent customer"""
        request = self.factory.get('/customers/999/')
        force_authenticate(request, user=self.nutritionist_user)
        response = self.view(request, customer_id=999)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Customer not found.')

    def test_get_customer_unauthorized(self):
        """Test GET request by unauthorized nutritionist"""
        request = self.factory.get(f'/customers/{self.customer.id}/')
        force_authenticate(request, user=self.other_nutritionist_user)
        response = self.view(request, customer_id=self.customer.id)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data['error'], 'You are not authorized to view this customer.')  # noqa:E501

    def test_update_customer_success(self):
        """Test successful POST request to update customer"""
        update_data = {
            'phone': '2222222222',
            'age': 26,
            'nutritional_goal': 'Weight loss'
        }
        request = self.factory.post(
            f'/customers/{self.customer.id}/',
            data=update_data,
            format='json'
        )
        force_authenticate(request, user=self.nutritionist_user)
        response = self.view(request, customer_id=self.customer.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.template_name,
            'dashboard/nutritionist_dashboard.html'
        )
        self.assertTrue(response.data['success'])
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.phone, '2222222222')
        self.assertEqual(self.customer.age, 26)

    def test_update_customer_unauthorized(self):
        """Test POST request by unauthorized nutritionist"""
        update_data = {'phone': '3333333333'}
        request = self.factory.post(
            f'/customers/{self.customer.id}/',
            data=update_data,
            format='json'
        )
        force_authenticate(request, user=self.other_nutritionist_user)
        response = self.view(request, customer_id=self.customer.id)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data['error'], 'You are not authorized to update this customer.')  # noqa:E501

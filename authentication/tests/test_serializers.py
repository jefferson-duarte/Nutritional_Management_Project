from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from authentication.serializers import (CustomerProfileSerializer,
                                        NutritionistProfileSerializer,
                                        UserSerializer)


class UserSerializerTest(TestCase):
    def setUp(self):
        self.user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'john@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }

    def test_create_user(self):
        serializer = UserSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, 'johndoe')
        self.assertEqual(user.email, 'john@example.com')

    def test_passwords_do_not_match(self):
        self.user_data['confirm_password'] = 'wrongpassword'
        serializer = UserSerializer(data=self.user_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_email_already_in_use(self):
        User.objects.create_user(
            username='existinguser', email='john@example.com', password='password123')  # noqa: E501
        serializer = UserSerializer(data=self.user_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_username_already_in_use(self):
        User.objects.create_user(
            username='johndoe', email='another@example.com', password='password123')  # noqa: E501
        serializer = UserSerializer(data=self.user_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


class NutritionistProfileSerializerTest(TestCase):
    def setUp(self):
        self.user_data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'username': 'janedoe',
            'email': 'jane@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }
        self.nutritionist_data = {
            'user': self.user_data,
            'registration_number': '12345',
            'phone': '1234567890'
        }

    def test_create_nutritionist_profile(self):
        serializer = NutritionistProfileSerializer(data=self.nutritionist_data)
        self.assertTrue(serializer.is_valid())
        nutritionist = serializer.save()
        self.assertEqual(nutritionist.registration_number, '12345')
        self.assertEqual(nutritionist.phone, '1234567890')
        self.assertEqual(nutritionist.user.username, 'janedoe')


class CustomerProfileSerializerTest(TestCase):
    def setUp(self):
        self.user_data = {
            'first_name': 'Alice',
            'last_name': 'Smith',
            'username': 'alicesmith',
            'email': 'alice@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }
        self.customer_data = {
            'user': self.user_data,
            'phone': '0987654321',
            'age': 30,
            'gender': 'F',
            'height': 1.65,
            'weight': 60,
            'nutritional_goal': 'Lose weight',
            'diet_plan': 'Low carb',
            'allergies': 'None',
            'last_appointment': '2023-01-01'
        }

    def test_create_customer_profile(self):
        serializer = CustomerProfileSerializer(data=self.customer_data)
        self.assertTrue(serializer.is_valid())
        customer = serializer.save()
        self.assertEqual(customer.phone, '0987654321')
        self.assertEqual(customer.age, 30)
        self.assertEqual(customer.user.username, 'alicesmith')

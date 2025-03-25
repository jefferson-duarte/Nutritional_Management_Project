from django.contrib.auth import get_user_model
from django.test import TestCase

from nutritional_plans.forms import NutritionalPlanForm

User = get_user_model()


class NutritionalPlanFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345')

    def test_nutritional_plan_form_valid(self):
        form_data = {
            'client': self.user.id,
            'title': 'Test Plan',
            'description': 'This is a test plan description.'
        }
        form = NutritionalPlanForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_nutritional_plan_form_invalid(self):
        form_data = {
            'client': '',
            'title': '',
            'description': ''
        }
        form = NutritionalPlanForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('client', form.errors)
        self.assertIn('title', form.errors)
        self.assertIn('description', form.errors)

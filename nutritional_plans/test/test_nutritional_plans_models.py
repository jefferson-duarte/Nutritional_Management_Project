from django.contrib.auth.models import User
from django.test import TestCase

from nutritional_plans.models import FoodItem, Meal, NutritionalPlan


class ModelStrTestCase(TestCase):
    def setUp(self):
        self.nutritionist = User.objects.create_user(
            username="nutri_user", password="testpass"
        )

        self.client = User.objects.create_user(
            username="client_user", password="testpass"
        )

        self.plan = NutritionalPlan.objects.create(
            nutritionist=self.nutritionist,
            client=self.client,
            title="Weight Loss Plan",
            description="A detailed plan for weight loss."
        )

        self.meal = Meal.objects.create(
            plan=self.plan,
            name="Breakfast",
            description="Oatmeal with fruits"
        )

        self.food_item = FoodItem.objects.create(
            meal=self.meal,
            name="Oats",
            quantity="50g"
        )

    def test_nutritional_plan_str(self):
        self.assertEqual(str(self.plan), "Weight Loss Plan")

    def test_meal_str(self):
        self.assertEqual(str(self.meal), "Breakfast")

    def test_food_item_str(self):
        self.assertEqual(str(self.food_item), "50g of Oats")

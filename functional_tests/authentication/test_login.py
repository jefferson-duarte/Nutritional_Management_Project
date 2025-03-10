from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from authentication.models import NutritionistProfile
from authentication.serializers import NutritionistProfileSerializer


class NutritionistRegistrationFunctionalTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Set up the WebDriver
        cls.browser = webdriver.Chrome()
        # Implicit wait of 10 seconds for elements to load
        cls.browser.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        # Close the browser after tests are done
        cls.browser.quit()
        super().tearDownClass()

    def test_nutritionist_registration_success(self):
        # Access the nutritionist registration page
        self.browser.get(
            self.live_server_url +
            reverse('register_nutritionist')
        )

        # Fill out the registration form
        first_name_input = self.browser.find_element(
            By.NAME, 'user[first_name]'
        )
        last_name_input = self.browser.find_element(By.NAME, 'user[last_name]')
        username_input = self.browser.find_element(By.NAME, 'user[username]')
        email_input = self.browser.find_element(By.NAME, 'user[email]')
        password_input = self.browser.find_element(By.NAME, 'user[password]')
        confirm_password_input = self.browser.find_element(
            By.NAME, 'user[confirm_password]'
        )
        registration_number_input = self.browser.find_element(
            By.NAME, 'registration_number'
        )
        phone_input = self.browser.find_element(By.NAME, 'phone')
        submit_button = self.browser.find_element(
            By.CSS_SELECTOR, 'button[type="submit"]'
        )

        # Enter valid data into the form
        first_name_input.send_keys('John')
        last_name_input.send_keys('Doe')
        username_input.send_keys('johndoe')
        email_input.send_keys('john@example.com')
        password_input.send_keys('password123')
        confirm_password_input.send_keys('password123')
        registration_number_input.send_keys('12345')
        phone_input.send_keys('1234567890')
        submit_button.click()

        # Verify that the user is redirected to the login page after successful registration  # noqa:E501
        WebDriverWait(self.browser, 10).until(
            EC.url_contains(reverse('login_create'))
        )
        self.assertIn(reverse('login_create'), self.browser.current_url)

        # Verify that the user and nutritionist profile were created in the database  # noqa:E501
        self.user = User.objects.get(username='johndoe')
        self.assertEqual(self.user.email, 'john@example.com')
        nutritionist_profile = NutritionistProfile.objects.get(user=self.user)
        self.assertEqual(nutritionist_profile.registration_number, '12345')
        self.assertEqual(nutritionist_profile.phone, '1234567890')

    def test_nutritionist_registration_failure(self):
        # Access the nutritionist registration page
        self.browser.get(
            self.live_server_url +
            reverse('register_nutritionist')
        )

        # Fill out the registration form with invalid data (passwords do not match)  # noqa:E501
        first_name_input = self.browser.find_element(
            By.NAME, 'user[first_name]'
        )
        last_name_input = self.browser.find_element(By.NAME, 'user[last_name]')
        username_input = self.browser.find_element(By.NAME, 'user[username]')
        email_input = self.browser.find_element(By.NAME, 'user[email]')
        password_input = self.browser.find_element(By.NAME, 'user[password]')
        confirm_password_input = self.browser.find_element(
            By.NAME, 'user[confirm_password]'
        )
        registration_number_input = self.browser.find_element(
            By.NAME, 'registration_number'
        )
        phone_input = self.browser.find_element(By.NAME, 'phone')
        submit_button = self.browser.find_element(
            By.CSS_SELECTOR, 'button[type="submit"]'
        )

        # Enter invalid data into the form
        first_name_input.send_keys('John')
        last_name_input.send_keys('Doe')
        username_input.send_keys('johndoe')
        email_input.send_keys('john@example.com')
        password_input.send_keys('password123')
        confirm_password_input.send_keys(
            'wrongpassword'  # Passwords do not match
        )
        registration_number_input.send_keys('12345')
        phone_input.send_keys('1234567890')
        submit_button.click()

        # Verify that an error message is displayed
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'alert-danger'))
        )
        error_message = self.browser.find_element(
            By.CLASS_NAME, 'alert-danger'
        )

        self.assertIn('Passwords do not match', error_message.text)

    def test_nutritionist_login_success(self):
        # Create a nutritionist profile and user in the database for login testing  # noqa:E501
        data = {
            'registration_number': '12345',
            'phone': '1234567890',
        }

        user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'john@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
        }
        data['user'] = user_data

        # Use the serializer to create the user and nutritionist profile
        serializer = NutritionistProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)

        # Access the login page
        self.browser.get(self.live_server_url + reverse('login_create'))

        # Fill out the login form
        username_input = self.browser.find_element(By.NAME, 'username')
        password_input = self.browser.find_element(By.NAME, 'password')
        submit_button = self.browser.find_element(
            By.CSS_SELECTOR, 'button[type="submit"]'
        )

        # Enter valid login credentials
        username_input.send_keys(user_data['username'])
        password_input.send_keys(user_data['password'])
        submit_button.click()

        # Verify that the user is redirected to the dashboard after successful login  # noqa:E501
        WebDriverWait(self.browser, 10).until(
            EC.url_contains(reverse('dashboard'))
        )
        self.assertIn(reverse('dashboard'), self.browser.current_url)

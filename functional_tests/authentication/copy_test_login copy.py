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
        # Configura o WebDriver (no exemplo, usamos o Chrome)
        cls.browser = webdriver.Chrome()  # Ou use webdriver.Firefox() para o Firefox # noqa:E501
        cls.browser.implicitly_wait(10)  # Espera implícita de 10 segundos

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def test_nutritionist_registration_success(self):
        # Acessa a página de registro de nutricionista
        self.browser.get(self.live_server_url + '/register/nutritionist/')  # Substitua pela URL correta # noqa:E501

        # Preenche o formulário de registro
        first_name_input = self.browser.find_element(By.NAME, 'user[first_name]')  # noqa:E501
        last_name_input = self.browser.find_element(By.NAME, 'user[last_name]')
        username_input = self.browser.find_element(By.NAME, 'user[username]')
        email_input = self.browser.find_element(By.NAME, 'user[email]')
        password_input = self.browser.find_element(By.NAME, 'user[password]')
        confirm_password_input = self.browser.find_element(By.NAME, 'user[confirm_password]')  # noqa:E501
        registration_number_input = self.browser.find_element(By.NAME, 'registration_number')   # noqa:E501
        phone_input = self.browser.find_element(By.NAME, 'phone')
        submit_button = self.browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]')  # noqa:E501

        first_name_input.send_keys('John')
        last_name_input.send_keys('Doe')
        username_input.send_keys('johndoe')
        email_input.send_keys('john@example.com')
        password_input.send_keys('password123')
        confirm_password_input.send_keys('password123')
        registration_number_input.send_keys('12345')
        phone_input.send_keys('1234567890')
        submit_button.click()

        # Verifica se o redirecionamento ocorreu corretamente
        WebDriverWait(self.browser, 10).until(
            EC.url_contains('login/create/')  # Substitua pela URL de redirecionamento após o registro  # noqa:E501
        )
        self.assertIn('login/create/', self.browser.current_url)

        # Verifica se o usuário e o perfil de nutricionista foram criados no banco de dados  # noqa:E501
        self.user = User.objects.get(username='johndoe')
        self.assertEqual(self.user.email, 'john@example.com')
        nutritionist_profile = NutritionistProfile.objects.get(user=self.user)
        self.assertEqual(nutritionist_profile.registration_number, '12345')
        self.assertEqual(nutritionist_profile.phone, '1234567890')

    def test_nutritionist_registration_failure(self):
        # Acessa a página de registro de nutricionista
        self.browser.get(self.live_server_url + '/register/nutritionist/')  # Substitua pela URL correta  # noqa:E501

        # Preenche o formulário de registro com dados inválidos (senhas não coincidem)  # noqa:E501
        first_name_input = self.browser.find_element(By.NAME, 'user[first_name]')  # noqa:E501
        last_name_input = self.browser.find_element(By.NAME, 'user[last_name]')
        username_input = self.browser.find_element(By.NAME, 'user[username]')
        email_input = self.browser.find_element(By.NAME, 'user[email]')
        password_input = self.browser.find_element(By.NAME, 'user[password]')
        confirm_password_input = self.browser.find_element(By.NAME, 'user[confirm_password]')  # noqa:E501
        registration_number_input = self.browser.find_element(By.NAME, 'registration_number')  # noqa:E501
        phone_input = self.browser.find_element(By.NAME, 'phone')
        submit_button = self.browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]')  # noqa:E501

        first_name_input.send_keys('John')
        last_name_input.send_keys('Doe')
        username_input.send_keys('johndoe')
        email_input.send_keys('john@example.com')
        password_input.send_keys('password123')
        confirm_password_input.send_keys('wrongpassword')  # Senhas não coincidem  # noqa:E501
        registration_number_input.send_keys('12345')
        phone_input.send_keys('1234567890')
        submit_button.click()

        # Verifica se a mensagem de erro é exibida
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'alert-danger'))
        )
        error_message = self.browser.find_element(By.CLASS_NAME, 'alert-danger')  # noqa:E501
        print(error_message.text)
        self.assertIn('Passwords do not match', error_message.text)

    def test_nutritionist_login_success(self):
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

        serializer = NutritionistProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)

        # Acessa a página de login
        self.browser.get(self.live_server_url + '/login/create/')

        # Preenche o formulário de login
        username_input = self.browser.find_element(By.NAME, 'username')
        password_input = self.browser.find_element(By.NAME, 'password')
        submit_button = self.browser.find_element(
            By.CSS_SELECTOR, 'button[type="submit"]'
        )

        username_input.send_keys(user_data['username'])
        password_input.send_keys(user_data['password'])
        submit_button.click()

        # Verifica se o redirecionamento ocorreu corretamente
        WebDriverWait(self.browser, 10).until(
            EC.url_contains(reverse('dashboard'))
        )
        self.assertIn(reverse('dashboard'), self.browser.current_url)

from django.test import TestCase
from django.urls import reverse, resolve
from .views import register, loginpage
from accounts.models import Customer
from django.contrib.auth.models import User
from .forms import CreateUserForm


class SignUpFormTest(TestCase):
    def test_form_has_fields(self):
        form = CreateUserForm()
        expected = ['username', 'name', 'email', 'password1', 'password2']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)


class SignUpViewTest(TestCase):
    def setUp(self):
        url = reverse('register')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve('/user/registrar')
        self.assertEquals(view.func, register)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, CreateUserForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 7)
        self.assertContains(self.response, 'type="text"', 2)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)


class InvalidSignUpTest(TestCase):
    def setUp(self):
        url = reverse('register')
        data = {
            'username': 'testador',
            'email': 'testador@gmail.com',
        }
        self.response = self.client.post(url, data)

    def test_sign_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_dont_user(self):
        self.assertFalse(User.objects.exists())


class SuccessfulSignupTest(TestCase):
    def setUp(self):
        url = reverse('register')
        data = {
            'username': 'testador123',
            'email': 'test@test.com',
            'password1': 'abcdef1234',
            'password2': 'abcdef1234',
        }
        self.response = self.client.post(url, data)
        self.login_url = reverse('loginpage')

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_redirection(self):
        self.assertRedirects(self.response, self.login_url)


class LoginViewTest(TestCase):
    def setUp(self):
        url = reverse('loginpage')
        self.response = self.client.get(url)

    def test_login_page_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_login_url_resolves_login_view(self):
        view = resolve('/user/login')
        self.assertEquals(view.func, loginpage)


class LoginSuccessfulTest(TestCase):
    def setUp(self):
        url = reverse('loginpage')
        data = {
            'username': 'testador3',
            'password': 'abcdef1234',
        }
        self.response = self.client.post(url, data)
        self.userpage = reverse('userpage')

    def test_redirection(self):
        self.assertRedirects(self.response, self.userpage)

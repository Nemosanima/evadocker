from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class TestFormsForAppUsers(TestCase):
    """Тесты для forms приложения users."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()

    def test_create_user_form(self):
        """Тест регистрации."""
        form_data = {'first_name': 'Harry',
                     'last_name': 'Potter',
                     'username': 'Lightning',
                     'email': 'harry@gmail.com',
                     'password1': '1r2rr3rrr',
                     'password2': '1r2rr3rrr'
                     }
        self.guest_client.post(reverse('users:signup'),
                               data=form_data,
                               follow=True)
        self.assertTrue(
            User.objects.filter(
                username='Lightning',
            ).exists()
        )

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

User = get_user_model()


class TestUrlsForAppUsers(TestCase):
    """Тесты для urls приложения users."""

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create(username='Nemo')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            '/auth/reset/done/': 'users/password_reset_complete.html',
            '/auth/reset/<uidb64>/<token>/': 'users/password_reset_confirm.html',
            '/auth/password_reset/done/': 'users/password_reset_done.html',
            '/auth/password_reset/': 'users/password_reset_form.html',
            '/auth/password_change/done/': 'users/password_change_done.html',
            '/auth/password_change/': 'users/password_change_form.html',
            '/auth/signup/': 'users/signup.html',
            '/auth/login/': 'users/login.html',
            f'/auth/profile/{self.user.username}/': 'users/profile.html',
            f'/auth/profile/{self.user.username}/posts/': 'users/profile_posts.html',
            f'/auth/profile/{self.user.username}/edit/': 'users/profile_edit.html',
            '/auth/follow/': 'users/follow.html',
            f'/auth/profile/{self.user.username}/followers/': 'users/profile_followers.html',
            f'/auth/profile/{self.user.username}/followings/': 'users/profile_followings.html',
            f'/auth/profile/{self.user.username}/delete/': 'users/profile_delete.html',
            '/auth/logout/': 'users/logged_out.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_guest_client_get_right_responses(self):
        """Проверка, что HTTP statuses для неавторизованного
        пользователя соответствуют ожиданиям
        """
        urls_responses = {
            '/auth/reset/done/': 200,
            '/auth/reset/<uidb64>/<token>/': 200,
            '/auth/password_reset/done/': 200,
            '/auth/password_reset/': 200,
            '/auth/password_change/done/': 302,
            '/auth/password_change/': 302,
            '/auth/signup/': 200,
            '/auth/login/': 200,
            f'/auth/profile/{self.user.username}/': 302,
            f'/auth/profile/{self.user.username}/posts/': 302,
            f'/auth/profile/{self.user.username}/edit/': 302,
            '/auth/follow/': 302,
            f'/auth/profile/{self.user.username}/followers/': 302,
            f'/auth/profile/{self.user.username}/followings/': 302,
            f'/auth/profile/{self.user.username}/delete/': 302,
            '/auth/logout/': 200,
        }
        for address, answer in urls_responses.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, answer)

    def test_authorized_client_get_right_responses(self):
        """Проверка, что HTTP statuses для авторизованного
        пользователя соответствуют ожиданиям
        """
        urls_responses = {
            '/auth/reset/done/': 200,
            '/auth/reset/<uidb64>/<token>/': 200,
            '/auth/password_reset/done/': 200,
            '/auth/password_reset/': 200,
            '/auth/password_change/done/': 200,
            '/auth/password_change/': 200,
            '/auth/signup/': 200,
            '/auth/login/': 200,
            f'/auth/profile/{self.user.username}/': 200,
            f'/auth/profile/{self.user.username}/posts/': 200,
            f'/auth/profile/{self.user.username}/edit/': 200,
            '/auth/follow/': 200,
            f'/auth/profile/{self.user.username}/followers/': 200,
            f'/auth/profile/{self.user.username}/followings/': 200,
            f'/auth/profile/{self.user.username}/delete/': 200,
            '/auth/logout/': 200,
        }
        for address, answer in urls_responses.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertEqual(response.status_code, answer)

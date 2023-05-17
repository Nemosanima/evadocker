from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Post
from users.models import Follow

User = get_user_model()


class TestViewsForAppUsers(TestCase):
    """Тесты views для приложения users."""

    def setUp(self):
        self.guest_client = Client()
        self.user_nemo = User.objects.create_user(username='Nemo', password='1n2nn3nnn')
        self.authorized_client = Client()
        self.authorized_client.force_login(user=self.user_nemo)

        self.user_harry = User.objects.create_user(username='Harry')
        self.authorized_client2 = Client()
        self.authorized_client2.force_login(user=self.user_harry)

        self.post = Post.objects.create(
            text='Тестовый пост',
            author=self.user_nemo
        )

    def test_views_uses_right_templates(self):
        """Тест, что views используют верные
        шаблоны.
        """
        views_templates = {
            reverse('users:signup'): 'users/signup.html',
            reverse('users:login'): 'users/login.html',
            reverse('users:password_change_form'): 'users/password_change_form.html',
            reverse('users:password_change_done'): 'users/password_change_done.html',
            reverse('users:password_reset_form'): 'users/password_reset_form.html',
            reverse('users:password_reset_done'): 'users/password_reset_done.html',
            reverse('users:password_reset_confirm',
                    kwargs={'uidb64': 'uidb64', 'token': 'token'}): 'users/password_reset_confirm.html',
            reverse('users:password_reset_complete'): 'users/password_reset_complete.html',
            reverse('users:profile',
                    kwargs={'username': self.user_nemo.username}): 'users/profile.html',
            reverse('users:profile_posts',
                    kwargs={'username': self.user_nemo.username}): 'users/profile_posts.html',
            reverse('users:profile_edit',
                    kwargs={'username': self.user_nemo.username}): 'users/profile_edit.html',
            reverse('users:follow'): 'users/follow.html',
            reverse('users:profile_followers',
                    kwargs={'username': self.user_nemo.username}): 'users/profile_followers.html',
            reverse('users:profile_followings',
                    kwargs={'username': self.user_nemo.username}): 'users/profile_followings.html',
            reverse('users:profile_delete',
                    kwargs={'username': self.user_nemo.username}): 'users/profile_delete.html',
            reverse('users:logout'): 'users/logged_out.html'
        }
        for view, template in views_templates.items():
            with self.subTest(view=view):
                response = self.authorized_client.get(view)
                self.assertTemplateUsed(response, template)

    def test_page_sign_up_uses_correct_template(self):
        """Проверка, что страница регистрации содержит правильную форму."""
        response = self.authorized_client.get(reverse('users:signup'))
        form_fields = {
            'first_name': forms.fields.CharField,
            'last_name': forms.fields.CharField,
            'username': forms.fields.CharField,
            'email': forms.fields.EmailField
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_page_profile_show_correct_context(self):
        """Тест, что для страницы index сформирован
        вернутый context.
        """
        response = self.authorized_client.get(reverse('users:profile',
                                                      kwargs={'username': self.user_nemo.username}))
        list_objects = response.context.get('page_obj')
        self.assertEqual(list_objects[0], self.post)

    def test_page_profile_posts_show_correct_context(self):
        """Тест, что для страницы profile_posts сформирован
        вернутый context.
        """
        response = response = self.authorized_client.get(reverse('users:profile_posts',
                                                         kwargs={'username': self.user_nemo.username}))

        list_objects = response.context.get('page_obj')
        self.assertEqual(list_objects[0], self.post)

    def test_page_profile_edit_show_correct_context(self):
        """Тест, что для страницы profile_edit сформирован
        вернутый context.
        """
        response = self.authorized_client.get(reverse('users:profile_edit',
                                                      kwargs={'username': self.user_nemo.username}))
        forms_fields = {
            'first_name': forms.fields.CharField,
            'last_name': forms.fields.CharField,
            'email': forms.fields.EmailField,
            'education': forms.fields.CharField,
            'work': forms.fields.CharField,
            'about_myself': forms.fields.CharField,
            'birth_date': forms.fields.DateField,
            'city': forms.fields.CharField
        }
        for value, expected in forms_fields.items():
            with self.subTest(value=value):
                field = response.context.get('form').fields.get(value)
                self.assertIsInstance(field, expected)

    def test_page_profile_delete_show_correct_context(self):
        """Тест, что для страницы profile_delete сформирован
        вернутый context.
        """
        response = self.authorized_client.get(reverse('users:profile_delete',
                                                      kwargs={'username': self.user_nemo.username}))
        field_password = response.context.get('form').fields.get('password')
        self.assertIsInstance(field_password, forms.fields.CharField)

    def test_user_can_delete_profile_with_right_password(self):
        """Тест, что user может удалить свой profile,
        если знает верный пароль.
        """
        self.assertTrue(
            User.objects.filter(
                username='Nemo'
            ).exists())
        form_data = {'password': '1n2nn3nnn'}
        self.authorized_client.post(reverse('users:profile_delete',
                                            kwargs={'username': self.user_nemo.username}),
                                    data=form_data,
                                    follow=True)
        self.assertFalse(
            User.objects.filter(
                username='Nemo'
            ).exists(), "Ошибка в 'test_user_can_delete_profile_with_right_password'")

    def test_user_cant_delete_profile_with_wrong_password(self):
        """Тест, что user не может удалить аккаунт с
        неверным паролем.
        """
        self.assertTrue(
            User.objects.filter(
                username='Nemo'
            ).exists())
        form_data = {'password': '123456789'}
        self.authorized_client.post(reverse('users:profile_delete',
                                            kwargs={'username': self.user_nemo.username}),
                                    data=form_data,
                                    follow=True)
        self.assertTrue(
            User.objects.filter(
                username='Nemo'
            ).exists(), "Ошибка в 'test_user_cant_delete_profile_with_wrong_password'")

    def test_user_can_follow_and_unfollow(self):
        """Тест, что авторизованный пользователь может подписывать и отписываться."""
        # проверка на подписку
        self.authorized_client.post(reverse('users:profile_follow',
                                            kwargs={'username': self.user_harry.username}))
        self.assertTrue(
            Follow.objects.filter(user=self.user_nemo,
                                  author=self.user_harry).exists())
        # проверка на отписку
        self.authorized_client.post(reverse('users:profile_unfollow',
                                            kwargs={'username': self.user_harry.username}))
        self.assertFalse(
            Follow.objects.filter(user=self.user_nemo,
                                  author=self.user_harry).exists())

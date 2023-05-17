from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from posts.models import Group, Post

User = get_user_model()


class TestUrlsForAppPosts(TestCase):
    """Тесты для urls приложения posts."""

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create(username='Nemo')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

        self.post = Post.objects.create(
            text='Тестовый пост',
            author=self.user,
        )

        self.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-group',
            description='Тестовое описание',
            admin=self.user
        )

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            '/search/': 'posts/search.html',
            '/': 'posts/index.html',
            f'/group/{self.group.slug}/': 'posts/group.html',
            '/groups_list/': 'posts/groups_list.html',
            f'/posts/{self.post.id}/': 'posts/post_detail.html',
            '/post_create/': 'posts/post_create.html',
            f'/posts/{self.post.id}/edit/': 'posts/post_create.html',
            '/group_create/': 'posts/group_create.html',
            f'/groups/{self.group.slug}/edit/': 'posts/group_edit.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_guest_client_get_right_responses(self):
        """Проверка, что HTTP statuses для неавторизованного
        пользователя соответствуют ожиданиям.
        """
        urls_responses = {
            '/search/': 302,
            '/': 200,
            f'/group/{self.group.slug}/': 200,
            '/groups_list/': 200,
            f'/posts/{self.post.id}/': 200,
            '/post_create/': 302,
            f'/posts/{self.post.id}/edit/': 302,
            '/group_create/': 302,
            f'/groups/{self.group.slug}/edit/': 302,
        }
        for address, answer in urls_responses.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, answer)

    def test_authorized_client_get_right_responses(self):
        """Проверка, что HTTP statuses для авторизованного
        пользователя соответствуют ожиданиям.
        """
        urls_responses = {
            '/search/': 200,
            '/': 200,
            f'/group/{self.group.slug}/': 200,
            '/groups_list/': 200,
            f'/posts/{self.post.id}/': 200,
            '/post_create/': 200,
            f'/posts/{self.post.id}/edit/': 200,
            '/group_create/': 200,
            f'/groups/{self.group.slug}/edit/': 200,
        }
        for address, answer in urls_responses.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertEqual(response.status_code, answer)

    def test_unexisting_page_response(self):
        """Проверк, что несущетвующий адрес вернет 404."""
        response = self.guest_client.get('/unexisting/page/')
        self.assertEqual(response.status_code, 404)

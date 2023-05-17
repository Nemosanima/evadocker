import shutil
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from posts.models import Comment, Group, Post

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class TestFormsForAppPosts(TestCase):
    """Тесты для forms приложения posts."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()

        cls.user_nemo = User.objects.create(username='Nemo')
        cls.user_harry = User.objects.create(username='Harry')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user_nemo)

        cls.ZERO_POSTS = Post.objects.count()
        cls.ZERO_GROUPS = Group.objects.count()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_post_create_authorized(self):
        """Тест создания поста."""
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        form_data = {
            'text': 'Тестовый пост',
            'image': uploaded,
            'author': self.user_nemo
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertEqual(self.ZERO_POSTS + 1, 1)
        self.assertRedirects(response, '/auth/profile/Nemo/posts/')
        self.assertTrue(
            Post.objects.filter(
                text='Тестовый пост'
            ).exists()
        )

    def test_post_create_unauthorized(self):
        """Тест создать пост не авторизовавшись."""
        form_data = {
            'text': 'Тестовый пост',
            'author': self.user_nemo
        }
        self.guest_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertEqual(self.ZERO_POSTS, 0)

    def test_delete_post_author(self):
        """Тест на возможность удалить пост автору."""
        self.post = Post.objects.create(
            text='Тестовый пост',
            author=self.user_nemo
        )
        self.assertEqual(self.ZERO_POSTS + 1, 1)
        self.authorized_client.post(
            reverse('posts:post_delete', kwargs={'post_id': self.post.id}),
            follow=True
        )
        self.assertEqual(self.ZERO_POSTS, 0)

    def test_delete_post_not_author(self):
        """Тест на возможность удалить пост не автору."""
        self.post = Post.objects.create(
            text='Тестовый пост',
            author=self.user_harry
        )
        self.assertEqual(self.ZERO_POSTS + 1, 1)
        self.authorized_client.post(
            reverse('posts:post_delete', kwargs={'post_id': self.post.id}),
            follow=True
        )
        self.assertEqual(self.ZERO_POSTS + 1, 1)

    def test_delete_post_unauthorized(self):
        """Тест на возможнсть удалить посте не авторизовавшись."""
        self.post = Post.objects.create(
            text='Тестовый пост',
            author=self.user_nemo
        )
        self.assertEqual(self.ZERO_POSTS + 1, 1)
        self.guest_client.post(
            reverse('posts:post_delete', kwargs={'post_id': self.post.id}),
            follow=True
        )
        self.assertEqual(self.ZERO_POSTS + 1, 1)

    def test_update_post_author(self):
        """Тест на возможность обновить пост автору."""
        post = Post.objects.create(
            text='Гарри Поттера написал Достоевский',
            author=self.user_nemo
        )
        self.assertEqual(self.ZERO_POSTS + 1, 1)

        form_data = {'text': 'Гарри Поттера написала Джоан Роулинг'}
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': post.id}),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, '/posts/1/')
        self.assertTrue(Post.objects.filter(
            text='Гарри Поттера написала Джоан Роулинг',
            author=self.user_nemo
        ).exists(), 'Автор не смог изменить пост')

    def test_update_post_not_author(self):
        """Тест на возможнсть обновть пост не автору."""
        post = Post.objects.create(
            text='Гарри Поттера написал Достоевский',
            author=self.user_harry
        )
        self.assertEqual(self.ZERO_POSTS + 1, 1)

        form_data = {'text': 'Гарри Поттера написала Джоан Роулинг'}
        self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': post.id}),
            data=form_data,
            follow=True
        )
        self.assertFalse(Post.objects.filter(
            text='Гарри Поттера написала Джоан Роулинг'
        ).exists(), 'Не автор смог изменить пост')

    def test_update_post_unauthorized(self):
        """Тест на возможнсть обрановить пост не авторизовавшись."""
        post = Post.objects.create(
            text='Гарри Поттера написал Достоевский',
            author=self.user_nemo
        )
        self.assertEqual(self.ZERO_POSTS + 1, 1)
        form_data = {'text': 'Гарри Поттера написала Джоан Роулинг'}
        self.guest_client.post(
            reverse('posts:post_edit', kwargs={'post_id': post.id}),
            data=form_data,
            follow=True
        )
        self.assertFalse(Post.objects.filter(
            text='Гарри Поттера написала Джоан Роулинг'
        ).exists(), 'Неавторизованный пользователь смог изменить пост')

    def test_create_group_authorized(self):
        """Тест на возможнсть создавть группу авторизовавшись."""
        form_data = {
            'title': 'Books',
            'slug': 'books',
            'description': 'about books',
            'admin': self.user_nemo
        }
        self.authorized_client.post(
            reverse('posts:group_create'),
            data=form_data,
            follow=True
        )
        self.assertEqual(self.ZERO_GROUPS + 1, 1)

    def test_create_group_unauthorized(self):
        """Тест на возможнсть создать группы не авторизовавшись."""
        form_data = {
            'title': 'Books',
            'slug': 'books',
            'description': 'about books',
            'admin': self.user_nemo
        }
        self.guest_client.post(
            reverse('posts:group_create'),
            data=form_data,
            follow=True
        )
        self.assertEqual(self.ZERO_GROUPS, 0)

    def test_update_group_admin(self):
        """Тест на возможнсть изменить группу админу."""
        group = Group.objects.create(
            title='Books',
            slug='books',
            description='about books',
            admin=self.user_nemo
        )
        self.assertEqual(self.ZERO_GROUPS + 1, 1)

        form_data = {'description': 'Новое описание группы'}
        response = self.authorized_client.post(
            reverse('posts:group_edit', kwargs={'group_slug': group.slug}),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, '/groups_list/')
        self.assertTrue(Group.objects.filter(
            description='Новое описание группы',
            admin=self.user_nemo
        ).exists(), 'Админ не смог изменить группу')

    def test_update_group_not_admin(self):
        """Тест на возможность изменить группу не админу."""
        group = Group.objects.create(
            title='Books',
            slug='books',
            description='about books',
            admin=self.user_harry
        )
        self.assertEqual(self.ZERO_GROUPS + 1, 1)

        form_data = {'description': 'Новое описание группы'}
        self.authorized_client.post(
            reverse('posts:group_edit', kwargs={'group_slug': group.slug}),
            data=form_data,
            follow=True
        )
        self.assertFalse(Group.objects.filter(
            description='Новое описание группы',
            admin=self.user_nemo
        ).exists(), 'Не админ смог изменить группу')

    def test_update_group_unauthorized(self):
        """Тест на возможнсть изменить группу не авторизовавшись."""
        group = Group.objects.create(
            title='Books',
            slug='books',
            description='about books',
            admin=self.user_nemo
        )
        self.assertEqual(self.ZERO_GROUPS + 1, 1)

        form_data = {'description': 'Новое описание группы'}
        self.guest_client.post(
            reverse('posts:group_edit', kwargs={'group_slug': group.slug}),
            data=form_data,
            follow=True
        )
        self.assertFalse(Group.objects.filter(
            description='Новое описание группы',
            admin=self.user_nemo
        ).exists(), 'Неавторизованный пользователь смог изменить группу')

    def test_create_comment_authorized(self):
        """Тест на возможноть написать комментарий
        авторизовавшись.
        """
        post = Post.objects.create(
            text='Новый пост',
            author=self.user_harry
        )
        form_data = {'text': 'Авторизированый'}
        self.authorized_client.post(reverse('posts:add_comment',
                                    kwargs={'post_id': post.id}),
                                    data=form_data,
                                    follow=True)
        self.assertTrue(
            Comment.objects.filter(
                text='Авторизированый'
            ).exists()
        )

    def test_create_comment_unauthorized(self):
        """Тест на возможноть написать комментарий
        не авторизовавшись.
        """
        post = Post.objects.create(
            text='Новый пост',
            author=self.user_harry
        )
        form_data = {'text': 'Неавторизированый'}
        self.guest_client.post(reverse('posts:add_comment',
                               kwargs={'post_id': post.id}),
                               data=form_data,
                               follow=True)
        self.assertFalse(
            Comment.objects.filter(
                text='Неавторизированый'
            ).exists()
        )

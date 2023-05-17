from django.contrib.auth import get_user_model
from django.test import TestCase

from posts.models import Comment, Group, Post

User = get_user_model()


class TestModelsForAppPosts(TestCase):
    """Тесты для models приложения posts."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='Nemo')
        cls.post = Post.objects.create(
            text='Тестовый пост',
            author=cls.user
        )
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-group',
            description='Тестовое описание',
            admin=cls.user
        )
        cls.comment = Comment.objects.create(
            post=cls.post,
            author=cls.user,
            text='Тестовый комментарий'
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей post, group, comment
        корректно работает __str__.
        """
        post = self.post
        expected = post.text[:15]
        self.assertEqual(expected, str(post))

        group = self.group
        expected = group.title
        self.assertEqual(expected, str(group))

        comment = self.comment
        expected = comment.text[:15]
        self.assertEqual(expected, str(comment))

    def test_verbose_name_for_post_model(self):
        """verbose_name в полях модели post
        совпадают с ожидаемыми.
        """
        post = self.post
        field_verboses = {
            'text': 'Текст поста',
            'author': 'Автор',
            'group': 'Группа',
            'created': 'Дата создания',
            'image': 'Изображение'
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name, expected_value)

    def test_verbose_name_for_group_model(self):
        """verbose_name в полях модели group
        совпадает с ожидаемым.
        """
        group = self.group
        field_verboses = {
            'title': 'Название группы',
            'slug': 'Адрес группы',
            'description': 'Описание группы',
            'created': 'Дата создания',
            'admin': 'Админ'
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    group._meta.get_field(field).verbose_name, expected_value)

    def test_verbose_name_for_comment_model(self):
        """verbose_name в полях модели comment
        совпадает с ожидаемым.
        """
        comment = self.comment
        field_verboses = {
            'post': 'Пост',
            'author': 'Автор',
            'text': 'Текст комментария',
            'created': 'Дата создания'
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    comment._meta.get_field(field).verbose_name, expected_value)

    def test_model_group_help_text_for_slug(self):
        group = self.group
        help_text = group._meta.get_field('slug').help_text
        self.assertEqual(help_text, 'Только на английском')

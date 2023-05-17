from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Comment, Group, Post

User = get_user_model()


class TestViewsForAppPosts(TestCase):
    """Тесты views для приложения posts."""

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create(username='Nemo')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

        self.group = Group.objects.create(
            title='Books',
            slug='books',
            description='about books',
            admin=self.user
        )
        self.post = Post.objects.create(
            text='Тестовый пост',
            author=self.user,
            group=self.group

        )
        self.form_fields_post = {
            'group': forms.models.ModelChoiceField,
            'text': forms.fields.CharField,
            'image': forms.fields.ImageField
        }
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            text='Тестовый комментарий'
        )

    def test_views_uses_right_templates(self):
        """Тест, что views используют верные
        шаблоны.
        """
        views_templates = {
            reverse('posts:search'): 'posts/search.html',
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group',
                    kwargs={'group_slug': self.group.slug}): 'posts/group.html',
            reverse('posts:groups_list'): 'posts/groups_list.html',
            reverse('posts:post_detail',
                    kwargs={'post_id': self.post.id}): 'posts/post_detail.html',
            reverse('posts:post_create'): 'posts/post_create.html',
            reverse('posts:post_edit',
                    kwargs={'post_id': self.post.id}): 'posts/post_create.html',
            reverse('posts:group_create'): 'posts/group_create.html',
            reverse('posts:group_edit',
                    kwargs={'group_slug': self.group.slug}): 'posts/group_edit.html'
        }
        for view, template in views_templates.items():
            with self.subTest(view=view):
                response = self.authorized_client.get(view)
                self.assertTemplateUsed(response, template)

    def test_page_index_show_correct_context(self):
        """Тест, что для страницы index сформирован
        вернутый context.
        """
        response = self.authorized_client.get(reverse('posts:index'))
        list_objects = response.context.get('page_obj')
        self.assertEqual(list_objects[0], self.post)

    def test_page_group_show_correct_context(self):
        """Тест, что для страницы group сформирован
        вернутый context.
        """
        response = self.authorized_client.get(reverse('posts:group',
                                              kwargs={'group_slug': self.group.slug}))
        list_objects = response.context.get('page_obj')
        self.assertEqual(list_objects[0], self.post)

    def test_page_groups_list_show_correct_context(self):
        """Тест, что для страницы groups_list сформирован
        вернутый context.
        """
        response = self.authorized_client.get(reverse('posts:groups_list'))
        list_objects = response.context.get('page_obj')
        self.assertEqual(list_objects[0], self.group)

    def test_page_post_detail_show_correct_context(self):
        """Тест, что для страницы post_detail
        cформирован правильный context.
        """
        response = self.authorized_client.get(reverse(
            'posts:post_detail', kwargs={'post_id': self.post.id}))
        post_object = response.context.get('post')
        form_object = response.context.get('form').fields.get('text')
        self.assertEqual(post_object, self.post)
        self.assertIsInstance(form_object, forms.fields.CharField)

    def test_page_post_creat_show_correct_context(self):
        """Тест, что для страницы post_create
        cформирован правильный context.
        """
        response = self.authorized_client.get(reverse('posts:post_create'))
        for value, expected in self.form_fields_post.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_page_post_edit_show_correct_context(self):
        """Тест, что для страницы post_edit
        cформирован правильный context.
        """
        response = self.authorized_client.get(reverse('posts:post_edit',
                                                      kwargs={'post_id': self.post.id}))

        for value, expected in self.form_fields_post.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_page_group_create_show_correct_context(self):
        """Тест, что для страницы group_create
        cформирован правильный context.
        """

        form_fields_group = {
            'title': forms.fields.CharField,
            'slug': forms.fields.SlugField,
            'description': forms.fields.CharField
        }
        response = self.authorized_client.get(reverse('posts:group_create'))
        for value, expected in form_fields_group.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_page_group_edit_show_correct_context(self):
        """Тест, что для страницы group_edit
        cформирован правильный context.
        """
        response = self.authorized_client.get(reverse('posts:group_edit',
                                                      kwargs={'group_slug': self.group.slug}))
        form_field = response.context.get('form').fields.get('description')
        self.assertIsInstance(form_field, forms.fields.CharField)

    def test_pages_paginator(self):
        """Проверка pagination."""
        for i in range(10):
            Post.objects.create(
                text='Тест pagination',
                author=self.user,
                group=self.group
            )
        ten_posts: int = 10
        one_post: int = 1

        for i in range(10):
            Group.objects.create(
                title=f'Test Pagination{i}',
                slug=f'pagination{i}',
                description='about pagination',
                admin=self.user
            )
        ten_groups: int = 10
        one_group: int = 1

        reverse_name_posts = {
            reverse('posts:index'): ten_posts,
            reverse('posts:index') + '?page=2': one_post,
            reverse('posts:group',
                    kwargs={'group_slug': self.group.slug}): ten_posts,
            reverse('posts:group',
                    kwargs={'group_slug': self.group.slug}) + '?page=2': one_post,
            reverse('posts:groups_list'): ten_groups,
            reverse('posts:groups_list') + '?page=2': one_group,
            reverse('posts:search'): ten_posts,
            reverse('posts:search') + '?page=2': one_post
        }
        for reverse_name, posts in reverse_name_posts.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertEqual(len(response.context['page_obj']), posts)

    def test_write_comment_can_only_authorized(self):
        """Тест, что написать комментарий может только
        авторизованый пользователь.
        """
        # проверка для неавторизованного пользователя
        form_data = {'text': 'Провека для комментария'}
        self.guest_client.post(reverse('posts:add_comment',
                                       kwargs={'post_id': self.post.id}),
                               data=form_data,
                               follow=True)
        self.assertFalse(
            Comment.objects.filter(
                text='Провека для комментария'
            ).exists()
        )
        # проверка для авторизованного пользователя
        self.authorized_client.post(reverse('posts:add_comment',
                                            kwargs={'post_id': self.post.id}),
                                    data=form_data,
                                    follow=True)
        self.assertTrue(
            Comment.objects.filter(
                text='Провека для комментария'
            ).exists()
        )

    def test_after_creation_comment_appears_on_page(self):
        """Тест, что после создания комментарии появляются
        на странице.
        """
        response = self.authorized_client.get(reverse('posts:post_detail',
                                                      kwargs={'post_id': self.post.id}))
        first_comment = response.context['comments'][0]
        self.assertEqual(first_comment, self.comment)

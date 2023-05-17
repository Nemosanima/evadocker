from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    education = models.CharField(
        verbose_name='Образование',
        max_length=50,
        blank=True
    )
    work = models.CharField(
        verbose_name='Работа',
        max_length=50,
        blank=True
    )
    about_myself = models.TextField(
        verbose_name='О себе',
        help_text='Расскажите о себе',
        max_length=500,
        blank=True
    )
    birth_date = models.DateField(
        verbose_name='Дата рождения',
        help_text='Дата рождения в формате: 10.10.2010',
        null=True,
        blank=True
    )
    city = models.CharField(
        verbose_name='Город',
        max_length=50,
        blank=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        related_name='followers',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        related_name='followings',
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ['user', 'author']
        ordering = ['-id']

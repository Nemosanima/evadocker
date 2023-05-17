from django.contrib import admin

from .models import Comment, Group, Post


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'author',
        'post',
        'created'
    )
    search_fields = ('author',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'admin',
        'slug',
        'description',
        'created'
    )
    search_fields = ('title',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'author',
        'group',
        'created',
        'image'
    )
    list_filter = ('created', 'author')
    search_fields = ('text',)
    list_editable = ('group',)

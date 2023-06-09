from django import forms

from .models import Comment, Group, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class GroupCreateForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('title', 'slug', 'description')


class GroupEditForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('description',)

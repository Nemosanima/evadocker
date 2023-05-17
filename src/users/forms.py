from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'education', 'work', 'about_myself', 'birth_date', 'city')


class ProfileDeleteForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('password',)

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from users.models import UserProfile, UserImage


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(label='User Name', max_length=64)
    password = forms.CharField(widget=forms.PasswordInput())


class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'first_name', 'last_name', 'birthday', 'about_user']
        help_texts = {
            'birthday': 'Input like, 1970-04-15',
        }


class UserImageForm(ModelForm):
    class Meta:
        model = UserImage
        fields = ['image', 'public']

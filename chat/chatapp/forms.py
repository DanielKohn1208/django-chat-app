from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class FriendForm(forms.Form):
    friendName = forms.CharField(
        label='Enter friend\'s username',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': "username"}
        )
    )


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Enter Username',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Username'}),
    )

    password = forms.CharField(
        label='Enter Password',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password1', 'password2',
        ]
    email = forms.EmailField(
        max_length=100,
        required=True,
        label='Your Email',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Email'}),
    )
    username = forms.CharField(
        max_length=200,
        required=True,
        label='Enter Username',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Username'}),
    )
    password1 = forms.CharField(
        label='Enter Password',
        required=True,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )
    password2 = forms.CharField(
        required=True,
        label='Enter Password Again',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password Again'}),
    )

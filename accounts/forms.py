from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *

from django.contrib.auth import get_user_model
User = get_user_model()


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    phone = forms.IntegerField()
    city = forms.CharField(max_length=100)

    class Meta:
        model = ShopUser
        fields = ('username', 'email')


class ShopUserCreationForm(UserCreationForm):

    class Meta:
        model = ShopUser
        # fields = ('username', 'email')
        fields = ('username', 'email','phone', 'city')



class ShopUserChangeForm(UserChangeForm):

    class Meta:
        model = ShopUser
        # fields = ('username', 'email')
        fields = ('username', 'email', 'phone', 'city')

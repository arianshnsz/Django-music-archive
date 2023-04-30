from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import Account


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = Account
        fields = ('username', 'first_name',
                  'last_name', 'password1', 'password2')

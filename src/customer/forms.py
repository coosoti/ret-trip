from django import forms
from django.contrib.auth.models import User

from src.models import Customer

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('avatar',)
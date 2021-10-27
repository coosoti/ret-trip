from django import forms
from django.contrib.auth.models import User
from django.forms import fields

from src.models import Customer, Task

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('avatar',)

class PackageInfoForm(forms.models.ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'description', 'category', 'size', 'quantity', 'image')
    
class PackagePickupForm(forms.models.ModelForm):
    pickup_address = forms.CharField(required=True)
    pickup_name = forms.CharField(required=True)
    pickup_phone = forms.CharField(required=True)
 
    class Meta:
        model = Task
        fields = ('pickup_address', 'pickup_lat', 'pickup_lng', 'pickup_name', 'pickup_phone')

class PackageDeliveryForm(forms.models.ModelForm):
    delivery_address = forms.CharField(required=True)
    delivery_name = forms.CharField(required=True)
    delivery_phone = forms.CharField(required=True)
 
    class Meta:
        model = Task
        fields = ('delivery_address', 'delivery_lat', 'delivery_lng', 'delivery_name', 'delivery_phone')
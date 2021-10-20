from django.contrib.auth import forms
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from django.contrib import messages
from src.customer import forms
@login_required()
def home(request):
    return redirect(reverse('customer:profile'))

@login_required(login_url="/login/?next=/customer/")
def profile(request):
    user_form = forms.UserForm(instance=request.user)
    customer_form = forms.CustomerForm(instance=request.user.customer)
    
    if request.method == "POST":
        user_form = forms.UserForm(request.POST, instance=request.user)
        customer_form = forms.CustomerForm(request.POST, request.FILES, instance=request.user.customer)
        if user_form.is_valid() and customer_form.is_valid():
            user_form.save()
            customer_form.save()
            messages.success(request, "You have successgully updated your profile")
            return redirect(reverse('customer:profile'))
    return render(request, 'customer/profile.html', {
        "user_form": user_form,
        "customer_form":customer_form
    })
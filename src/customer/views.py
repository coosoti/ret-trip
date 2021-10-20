from django.contrib.auth import forms
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from src.customer import forms
@login_required()
def home(request):
    return redirect(reverse('customer:profile'))

@login_required(login_url="/login/?next=/customer/")
def profile(request):
    user_form = forms.UserForm(instance=request.user)
    
    if request.method == "POST":
        user_form = forms.UserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect(reverse('customer:profile'))
    return render(request, 'customer/profile.html', {
        "user_form": user_form
    })
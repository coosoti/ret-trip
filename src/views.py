from django.contrib.auth import forms
from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from . import forms

def home(request):
    return render(request, 'index.html')

@login_required()
def customer_page(request):
    return render(request, 'index.html')

@login_required()
def driver_page(request):
    return render(request, 'index.html')

def register(request):
    form = forms.RegisterationForm()

    if request.method == 'POST':
        form = forms.RegisterationForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email').lower()
            user = form.save(commit=False)
            user.username = email
            user.save()

            login(request, user)
            return redirect('/')

    return render(request, 'register.html', {
        'form': form
    })
 
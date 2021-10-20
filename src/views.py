from django.contrib.auth import forms
from django.shortcuts import redirect, render
from django.contrib.auth import login


from . import forms

def home(request):
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

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/')

    return render(request, 'register.html', {
        'form': form
    })
 
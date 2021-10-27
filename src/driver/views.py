from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.conf import settings

@login_required(login_url="/login/?next=/driver/")
def home(request):
    return redirect(reverse('driver:available_tasks'))

@login_required(login_url="/login/?next=/driver/")
def available_tasks(request):
    return render(request, 'driver/available_tasks.html', {
        "GOOGLE_MAP_API_KEY": settings.GOOGLE_MAP_API_KEY,
    })
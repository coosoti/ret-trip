from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.conf import settings

from src.models import *

@login_required(login_url="/login/?next=/driver/")
def home(request):
    return redirect(reverse('driver:available_tasks'))

@login_required(login_url="/login/?next=/driver/")
def available_tasks(request):
    return render(request, 'driver/available_tasks.html', {
        "GOOGLE_MAP_API_KEY": settings.GOOGLE_MAP_API_KEY,
    })

@login_required(login_url="/login/?next=/driver/")
def available_task(request, id):
    task = Task.objects.filter(id=id, status=Task.PROCESSING_STATUS).last()

    if not task:
        return redirect(reverse('driver:available_tasks'))

    if request.method == "POST":
        task.driver = request.user.driver
        task.status = Task.PICKING_STATUS
        task.save()

        return redirect(reverse('driver:available_tasks'))
        
    return render(request, 'driver/available_task.html', {
        "task": task,
    })

@login_required(login_url="/login/?next=/driver/")
def current_task(request):
    task = Task.objects.filter(
        driver=request.user.driver, 
        status__in = [
            Task.PICKING_STATUS,
            Task.DELIVERING_STATUS
        ]
    ).last()
   
    return render(request, 'driver/current_task.html', {
        "task": task,
        "GOOGLE_MAP_API_KEY": settings.GOOGLE_MAP_API_KEY,
    })

@login_required(login_url="/login/?next=/driver/")
def photo_evidence(request, id):
    task = Task.objects.filter(
        id=id,
        driver=request.user.driver,
        status__in = [
            Task.PICKING_STATUS,
            Task.DELIVERING_STATUS
        ]
    ).last()

    if not task:
        return redirect(reverse('driver:current_task'))
    
    return render(request, 'driver/take_photo.html', {
        "task": task,
    })
  
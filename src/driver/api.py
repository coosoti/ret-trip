from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from src.models import *

@csrf_exempt
@login_required(login_url="/driver/login/")
def available_tasks_api(request):
    tasks = list(Task.objects.filter(status=Task.PROCESSING_STATUS).values())

    return JsonResponse({
        "success": True,
        "tasks": tasks,
    })


@csrf_exempt
@login_required(login_url="/driver/login/")
def current_task_update_api(request, id):
    task = Task.objects.filter(
        id=id,
        driver=request.user.driver,
        status__in=[
            Task.PICKING_STATUS,
            Task.DELIVERING_STATUS
        ]
    ).last()

    if task.status == Task.PICKING_STATUS:
        task.pickup_photo = request.FILES['pickup_photo']
        task.pickedup_at = timezone.now()
        task.status = Task.DELIVERING_STATUS
        task.save()

    elif task.status == Task.DELIVERING_STATUS:
        task.delivery_photo = request.FILES['delivery_photo']
        task.delivered_at = timezone.now()
        task.status = Task.COMPLETED_STATUS
        task.save()

    return JsonResponse({
        "success": True,
    })

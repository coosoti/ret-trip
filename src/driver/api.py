from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
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

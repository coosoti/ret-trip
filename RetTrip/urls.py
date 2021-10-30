"""RetTrip URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from src import views
from src.customer import views as customer_views
from src.driver import views as driver_views, api as driver_api

customer_urlpatterns = [
    path('', customer_views.home, name="home"),
    path('profile/', customer_views.profile, name="profile"),
    path('payment_method/', customer_views.payment_method, name="payment_method"),
    path('create_task/', customer_views.create_task, name="create_task"),

    path('tasks/current/', customer_views.current_tasks, name="current_tasks"),
    path('tasks/archived/', customer_views.archived_tasks, name="archived_tasks"),
    path('tasks/<task_id>/', customer_views.task_page, name="task"),
]
 
driver_urlpatterns = [
    path('', driver_views.home, name="home"),
    path('tasks/available/', driver_views.available_tasks, name="available_tasks"),
    path('tasks/available/<id>/', driver_views.available_task, name="available_task"),
    path('tasks/current/', driver_views.current_task, name="current_task"),
    path('tasks/current/<id>/photo_evidence/', driver_views.photo_evidence, name="photo_evidence"),

    path('api/v1/tasks/available/', driver_api.available_tasks_api, name="available_tasks_api"),
    path('api/v1/tasks/current/<id>/update', driver_api.current_task_update_api, name="current_task_update_api"),
] 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('social_django.urls', namespace='social')),
    path('', views.home),

    path('login/', auth_views.LoginView.as_view(template_name="login.html")),
    path('logout/', auth_views.LogoutView.as_view(next_page="/")),
    path('register/', views.register),

    path('customer/', include((customer_urlpatterns, 'customer'))),
    path('driver/', include((driver_urlpatterns, 'driver'))),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

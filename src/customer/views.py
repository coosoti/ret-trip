import requests
import stripe
from django.contrib.auth import forms
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.conf import settings

import firebase_admin
from firebase_admin import auth, credentials

from src.customer import forms
from src.models import *

cred = credentials.Certificate(settings.FIREBASE_ADMIN_CREDENTIAL)
firebase_admin.initialize_app(cred)

stripe.api_key = settings.STRIPE_API_SECRET_KEY

@login_required() 
def home(request):
    return redirect(reverse('customer:profile'))

@login_required(login_url="/login/?next=/customer/")
def profile(request):
    user_form = forms.UserForm(instance=request.user)
    customer_form = forms.CustomerForm(instance=request.user.customer)
    password_form = PasswordChangeForm(request.user)
    
    if request.method == "POST":
        if request.POST.get('action') == 'update_profile':
            user_form = forms.UserForm(request.POST, instance=request.user)
            customer_form = forms.CustomerForm(request.POST, request.FILES, instance=request.user.customer)
            if user_form.is_valid() and customer_form.is_valid():
                user_form.save()
                customer_form.save()
                messages.success(request, "You have successfully updated your profile")
                return redirect(reverse('customer:profile'))
        
        elif request.POST.get('action') == 'update_password':
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)

                messages.success(request, "You have successfully updated your password")
                return redirect(reverse('customer:profile'))
        
        elif request.POST.get('action') == 'update_phone_no':
            fb_user = auth.verify_id_token(request.POST.get("id_token"))

            request.user.customer.phone_no = fb_user['phone_number']
            request.user.customer.save()
            return redirect(reverse('customer:profile'))
            
    return render(request, 'customer/profile.html', {
        "user_form": user_form,
        "customer_form": customer_form,
        "password_form": password_form
    })

@login_required(login_url="/login/?next=/customer/")
def payment_method(request):
    current_customer = request.user.customer

    # Removing an existing card details
    if request.method == "POST":
        stripe.PaymentMethod.detach(current_customer.stripe_payment_method_id)
        current_customer.stripe_payment_method_id  = ""
        current_customer.stripe_card_last4 = ""
        current_customer.save()
        return redirect(reverse('customer:payment_method'))

    # saving current stripe customer info
    if not current_customer.stripe_customer_id:
        customer = stripe.Customer.create()
        current_customer.stripe_customer_id = customer['id']
        current_customer.save()
    
    # Getting the stripe payment method of the customer
    stripe_payment_methods = stripe.PaymentMethod.list(
        customer = current_customer.stripe_customer_id,
        type = "card",
    )

    print(stripe_payment_methods)

    if stripe_payment_methods and len(stripe_payment_methods.data) > 0:
        payment_method = stripe_payment_methods.data[0]
        current_customer.stripe_payment_method_id = payment_method.id
        current_customer.stripe_card_last4 = payment_method.card.last4
        current_customer.save()

    else:
        current_customer.stripe_payment_method_id = ""
        current_customer.stripe_card_last4 = ""
        current_customer.save()

    if not current_customer.stripe_payment_method_id:
        intent = stripe.SetupIntent.create(
            customer = current_customer.stripe_customer_id
        ) 
        return render(request, 'customer/payment.html', {
            "client_secret": intent.client_secret,
            "STRIPE_API_PUBLIC_KEY": settings.STRIPE_API_PUBLIC_KEY,
        })
    else:
        return render(request, 'customer/payment.html')

@login_required(login_url="/login/?next=/customer/")
def create_task(request):
    current_customer = request.user.customer
    if not current_customer.stripe_payment_method_id:
        return redirect(reverse('customer:payment_method'))


    cs_has_current_task = Task.objects.filter(
        customer = current_customer,
        status__in = [
            Task.PROCESSING_STATUS,
            Task.PICKING_STATUS,
            Task.DELIVERING_STATUS
        ]
    ).exists()

    if cs_has_current_task:
        messages.warning(request, "You have a task currently in progress")
        return redirect(reverse('customer:current_tasks'))

    creating_task = Task.objects.filter(customer = current_customer, status=Task.CREATING_STATUS).last()

    packageInfo_form = forms.PackageInfoForm(instance=creating_task)
    packagePickup_form = forms.PackagePickupForm(instance=creating_task)
    packageDelivery_form = forms.PackageDeliveryForm(instance=creating_task)
    
    if request.method == "POST":
        if request.POST.get('step') == '1':
            packageInfo_form = forms.PackageInfoForm(request.POST, request.FILES, instance=creating_task)
            if packageInfo_form.is_valid():
                creating_task = packageInfo_form.save(commit=False)
                creating_task.customer = current_customer
                creating_task.save()
                return redirect(reverse('customer:create_task'))

        elif request.POST.get('step') == '2':
            packagePickup_form = forms.PackagePickupForm(request.POST, instance=creating_task)
            if packagePickup_form.is_valid():
                creating_task = packagePickup_form.save()
                return redirect(reverse('customer:create_task'))

        elif request.POST.get('step') == '3':
            packageDelivery_form = forms.PackageDeliveryForm(request.POST, instance=creating_task)
            if packageDelivery_form.is_valid():
                creating_task = packageDelivery_form.save()
                try:
                    rq = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json?origins={}&destinations={}&transit_mode=bus&key={}".format(
                        creating_task.pickup_address,
                        creating_task.delivery_address,
                        settings.GOOGLE_MAP_API_KEY,
                    ))

                    print(rq.json()['rows'])

                    distance = rq.json()['rows'][0]['elements'][0]['distance']['value']
                    duration = rq.json()['rows'][0]['elements'][0]['duration']['value']
                    creating_task.distance = round(distance / 1000, 2)
                    creating_task.duration = int(duration / 60)
                    creating_task.price = creating_task.distance * .50
                    creating_task.save()
                except Exception as e:
                    print(e)
                    messages.error(request, "Unfortunately, we do not deliver to Mars")
                return redirect(reverse('customer:create_task'))

        elif request.POST.get('step') == '4':
            if creating_task.price:
                try:
                    payment_intent = stripe.PaymentIntent.create(
                        amount=int(creating_task.price * 100),
                        currency='kes',
                        customer=current_customer.stripe_customer_id,
                        payment_method=current_customer.stripe_payment_method_id,
                        off_session=True,
                        confirm=True,
                    )

                    Transaction.objects.create(
                        stripe_payment_intent_id = payment_intent['id'],
                        task = creating_task,
                        amount = creating_task.price,
                    )

                    creating_task.status = Task.PROCESSING_STATUS
                    creating_task.save()

                    return redirect(reverse('customer:home'))

                except stripe.error.CardError as e:
                    err = e.error
                    # Error code will be authentication_required if authentication is needed
                    print("Code is: %s" % err.code)
                    payment_intent_id = err.payment_intent['id']
                    payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
    #
    if not creating_task:
        current_step = 1  
    elif creating_task.delivery_name:
        current_step = 4
    elif creating_task.pickup_name:
        current_step = 3
    else:
        current_step = 2

    return render(request, 'customer/create_task.html', {
        "packageInfo_form": packageInfo_form,
        "packagePickup_form": packagePickup_form,
        "packageDelivery_form": packageDelivery_form,
        "task": creating_task,
        "step": current_step,
        "GOOGLE_MAP_API_KEY": settings.GOOGLE_MAP_API_KEY,
    })

@login_required(login_url="/login/?next=/customer/")
def current_tasks(request):
    tasks = Task.objects.filter(
        customer=request.user.customer,
        status__in=[
            Task.PROCESSING_STATUS,
            Task.PICKING_STATUS,
            Task.DELIVERING_STATUS
        ]
    )

    return render(request, 'customer/tasks.html', {
        "tasks": tasks,
    })

@login_required(login_url="/login/?next=/customer/")
def archived_tasks(request):
    tasks = Task.objects.filter(
        customer=request.user.customer,
        status__in=[
            Task.COMPLETED_STATUS,
            Task.CANCELED_STATUS
        ]
    )

    return render(request, 'customer/tasks.html', {
        "tasks": tasks,
    }) 

@login_required(login_url="/login/?next=/customer/")
def task_page(request, task_id):
    task = Task.objects.get(id=task_id)

    if request.method == "POST" and task.status == Task.PROCESSING_STATUS:
        task.status = Task.CANCELED_STATUS
        task.save()
        return redirect(reverse('customer:archived_tasks'))

    return render(request, 'customer/task.html', {
        "task": task,
        "GOOGLE_MAP_API_KEY": settings.GOOGLE_MAP_API_KEY,
    })
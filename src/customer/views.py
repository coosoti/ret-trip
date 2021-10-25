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
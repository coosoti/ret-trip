import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey
from django.utils import timezone


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='customer/avatars/', blank=True, null=True)
    phone_no = models.CharField(max_length=15, blank=True)
    stripe_customer_id = models.CharField(max_length=255, blank=True)
    stripe_payment_method_id = models.CharField(max_length=255, blank=True)
    stripe_card_last4 = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return self.user.get_full_name()

class Category(models.Model):
    slug = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Task(models.Model):
    SMALL_SIZE = 'small'
    MEDIUM_SIZE = 'medium'
    LARGE_SIZE = 'large'
    SIZES = (
        (SMALL_SIZE, 'Small'),
        (MEDIUM_SIZE, 'Medium'),
        (LARGE_SIZE, 'Large'),
    )

    CREATING_STATUS = 'creating'
    PROCESSING_STATUS = 'processing'
    PICKING_STATUS = 'picking'
    DELIVERING_STATUS = 'delivering'
    COMPLETED_STATUS = 'completed'
    CANCELED_STATUS = 'canceled'
    STATUSES = (
        (CREATING_STATUS, 'Creating'),
        (PROCESSING_STATUS, 'Processing'),
        (PICKING_STATUS, 'Picking'),
        (DELIVERING_STATUS, 'Delivering'),
        (COMPLETED_STATUS, 'Completed'),
        (CANCELED_STATUS, 'Canceled'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    category = ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    size = models.CharField(max_length=30, choices=SIZES, default=MEDIUM_SIZE)
    quantity = models.IntegerField(default=1)
    image = models.ImageField(upload_to='task/images/')
    status = models.CharField(max_length=30, choices=STATUSES, default=CREATING_STATUS)
    created_at = models.DateTimeField(default=timezone.now)

    pickup_address = models.CharField(max_length=255, blank=True)
    pickup_lat = models.FloatField(default=0)
    pickup_lng = models.FloatField(default=0)
    pickup_name = models.CharField(max_length=255, blank=True)
    pickup_phone = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.name
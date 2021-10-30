import uuid
from django.db import DefaultConnectionProxy, models
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

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lat = models.FloatField(default=0)
    lng = models.FloatField(default=0)
    
    def __str__(self):
        return self.user.get_full_name()


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
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    category = ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    size = models.CharField(max_length=30, choices=SIZES, default=MEDIUM_SIZE)
    quantity = models.IntegerField(default=1)
    image = models.ImageField(upload_to='task/images/')
    status = models.CharField(max_length=30, choices=STATUSES, default=CREATING_STATUS)
    created_at = models.DateTimeField(default=timezone.now)

    # Pickup Details
    pickup_address = models.CharField(max_length=255, blank=True)
    pickup_lat = models.FloatField(default=0)
    pickup_lng = models.FloatField(default=0)
    pickup_name = models.CharField(max_length=255, blank=True)
    pickup_phone = models.CharField(max_length=30, blank=True)

    # Delivery Details
    delivery_address = models.CharField(max_length=255, blank=True)
    delivery_lat = models.FloatField(default=0)
    delivery_lng = models.FloatField(default=0)
    delivery_name = models.CharField(max_length=255, blank=True)
    delivery_phone = models.CharField(max_length=30, blank=True)

    # Payment Details
    duration = models.IntegerField(default=0)
    distance = models.FloatField(default=0)
    price = models.FloatField(default=0)

    pickup_photo = models.ImageField(upload_to='tasks/pickup_photos/', null=True, blank=True)
    pickedup_at = models.DateTimeField(null=True, blank=True)

    delivery_photo = models.ImageField(upload_to='tasks/delivery_photos/', null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    stripe_payment_intent_id = models.CharField(max_length=255, unique=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.stripe_payment_intent_id
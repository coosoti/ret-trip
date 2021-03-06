# Generated by Django 3.1.3 on 2021-10-26 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0009_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='delivered_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='delivery_photo',
            field=models.ImageField(blank=True, null=True, upload_to='tasks/delivery_photos/'),
        ),
        migrations.AddField(
            model_name='task',
            name='pickedup_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='pickup_photo',
            field=models.ImageField(blank=True, null=True, upload_to='tasks/pickup_photos/'),
        ),
    ]

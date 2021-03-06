# Generated by Django 3.1.3 on 2021-10-26 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0006_auto_20211025_1151'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='delivery_address',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='task',
            name='delivery_lat',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='task',
            name='delivery_lng',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='task',
            name='delivery_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='task',
            name='delivery_phone',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]

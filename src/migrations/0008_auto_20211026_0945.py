# Generated by Django 3.1.3 on 2021-10-26 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0007_auto_20211026_0752'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='distance',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='task',
            name='duration',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='task',
            name='price',
            field=models.FloatField(default=0),
        ),
    ]

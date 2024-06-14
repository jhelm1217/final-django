# Generated by Django 5.0.6 on 2024-06-13 13:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_final', '0003_trip_created_by'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='trip',
            name='friends',
            field=models.ManyToManyField(blank=True, null=True, related_name='shared_trips', to=settings.AUTH_USER_MODEL),
        ),
    ]

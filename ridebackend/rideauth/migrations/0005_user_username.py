# Generated by Django 5.0.7 on 2024-08-19 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rideauth', '0004_remove_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]

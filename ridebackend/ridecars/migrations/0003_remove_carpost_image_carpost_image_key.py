# Generated by Django 5.0.7 on 2024-09-02 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ridecars', '0002_alter_carpost_door_number_alter_carpost_gear_number_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carpost',
            name='image',
        ),
        migrations.AddField(
            model_name='carpost',
            name='image_key',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

# Generated by Django 5.0.7 on 2024-09-20 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ridecars', '0005_remove_carpost_image_id_remove_carpost_image_key'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carpost',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='carpost',
            name='contact',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

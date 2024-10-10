# Generated by Django 5.0.7 on 2024-09-15 13:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ridecars", "0004_carpost_image_id"),
        ("rideposts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="file",
            name="post",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="ridecars.carpost",
            ),
        ),
    ]

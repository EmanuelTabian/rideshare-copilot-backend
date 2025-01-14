# Generated by Django 5.0.7 on 2024-08-13 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ridecalc", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="calculatorentry",
            name="earnings",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=10,
                null=True,
                verbose_name="Earnings",
            ),
        ),
        migrations.AlterField(
            model_name="calculatorentry",
            name="expenses",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=10,
                null=True,
                verbose_name="Expenses",
            ),
        ),
    ]

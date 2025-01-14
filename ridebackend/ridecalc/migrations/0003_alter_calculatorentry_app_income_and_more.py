# Generated by Django 5.0.7 on 2024-08-13 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ridecalc", "0002_calculatorentry_earnings_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="calculatorentry",
            name="app_income",
            field=models.DecimalField(
                decimal_places=2, max_digits=10, verbose_name="App income"
            ),
        ),
        migrations.AlterField(
            model_name="calculatorentry",
            name="commission",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=10,
                null=True,
                verbose_name="Commission",
            ),
        ),
    ]

from decimal import Decimal

from django import forms
from django.contrib import admin

from .models import CalculatorEntry


class CalculatorForm(forms.ModelForm):

    class Meta:
        model = CalculatorEntry
        fields = ("user", "app_income", "commission", "expenses")


class CalculatorAdmin(admin.ModelAdmin):
    form = CalculatorForm
    list_display = (
        "user",
        "id",
        "app_income",
        "commission",
        "expenses",
        "earnings",
        "pub_date",
    )
    list_display_links = ("user", "id")
    search_fields = ("user", "app_income", "pub_date", "commission")
    list_per_page = 25

    def save_model(self, request, obj, form, change):
        commission = obj.commission if obj.commission is not None else Decimal(0)
        expenses = obj.expenses if obj.expenses is not None else Decimal(0)

        obj.earnings = obj.app_income - (commission / 100) * obj.app_income - expenses
        super().save_model(request, obj, form, change)


admin.site.register(CalculatorEntry, CalculatorAdmin)

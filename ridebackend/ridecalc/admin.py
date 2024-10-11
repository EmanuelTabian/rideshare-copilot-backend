from .models import CalculatorEntry
from django import forms

from django.contrib import admin

class UserChangeForm(forms.ModelForm):

    class Meta:
        model = CalculatorEntry
        fields = ("user", "app_income",'commission', 'expenses', 'earnings')

  
class CalculatorAdmin(admin.ModelAdmin):
    form = UserChangeForm
    list_display = ("id","app_income", "commission", "expenses", "earnings", "pub_date")
    list_display_links = ("id", "app_income")
    search_fields = ("app_income", "pub_date", "commission")
    list_per_page = 25

admin.site.register(CalculatorEntry, CalculatorAdmin)

from django.contrib import admin
from django import forms
from .models import User

class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name','email', 'username')

class UserAdmin(admin.ModelAdmin):
    form = UserChangeForm
    list_display = ("id", "name", "email", "username")
    list_display_links = ("id", "name")
    search_fields = ("name", "email", "username")
    list_per_page = 25

admin.site.register(User, UserAdmin)

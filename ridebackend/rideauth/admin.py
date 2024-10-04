from django.contrib import admin
from django import forms
from .models import User

class UserChangeForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False, help_text="Leave blank for no modification.")
    class Meta:
        model = User
        fields = ('email','name', 'password')

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data["password"]:
            user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UserAdmin(admin.ModelAdmin):
    form = UserChangeForm
    list_display = ("id", "name", "email", "username")
    list_display_links = ("id", "name")
    search_fields = ("name", "email", "username")
    list_per_page = 25

admin.site.register(User, UserAdmin)

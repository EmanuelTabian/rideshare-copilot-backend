from django.urls import path
from .views import AddCalculatorEntry,GetCalculatorEntries

urlpatterns = [
    path('add-calculator-entry', AddCalculatorEntry.as_view()),
    path('get-calculator-entries', GetCalculatorEntries.as_view())
]
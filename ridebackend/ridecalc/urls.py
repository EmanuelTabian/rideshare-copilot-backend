from django.urls import path
from .views import AddCalculatorEntry,GetCalculatorEntries,UpdateCalculatorEntries

urlpatterns = [
    path('add-calculator-entry', AddCalculatorEntry.as_view()),
    path('get-calculator-entries', GetCalculatorEntries.as_view()),
    path('update-calculator-entry/<int:calcentry_id>', UpdateCalculatorEntries.as_view())
]
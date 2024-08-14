from django.urls import path
from .views import AddCalculatorEntry,GetCalculatorEntries,UpdateCalculatorEntries,DeleteCalculatorEntries

urlpatterns = [
    path('add-calculator-entry', AddCalculatorEntry.as_view()),
    path('get-calculator-entries', GetCalculatorEntries.as_view()),
    path('update-calculator-entry/<int:calcentry_id>', UpdateCalculatorEntries.as_view()),
     path('delete-calculator-entry/<int:calcentry_id>', DeleteCalculatorEntries.as_view())
]
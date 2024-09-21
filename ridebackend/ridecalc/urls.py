from django.urls import path

from .views import (AddCalculatorEntry, DeleteCalculatorEntry,
                    GetCalculatorEntries, UpdateCalculatorEntry)

urlpatterns = [
    path('add-calculator-entry', AddCalculatorEntry.as_view()),
    path('get-calculator-entries', GetCalculatorEntries.as_view()),
    path('update-calculator-entry/<int:calcentry_id>', UpdateCalculatorEntry.as_view()),
    path('delete-calculator-entry/<int:calcentry_id>', DeleteCalculatorEntry.as_view())
]
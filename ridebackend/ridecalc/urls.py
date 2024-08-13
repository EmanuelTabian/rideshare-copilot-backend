from django.urls import path
from .views import AddCalculatorEntry

urlpatterns = [
    path('add-calculator-entry', AddCalculatorEntry.as_view())
]
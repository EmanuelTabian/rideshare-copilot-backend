from django.db import models
from rideauth.models import User

# Create your models here.
class CalculatorEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('Entry date', auto_now_add=True)
    app_income = models.DecimalField("App income" ,max_digits=5, decimal_places=2)
    commission = models.DecimalField("Commission" ,max_digits=5, decimal_places=2)
    expenses = models.DecimalField("Expenses" ,max_digits=5, decimal_places=2)


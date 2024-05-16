from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class StockSymbol(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=15)
    description = models.TextField()
    currency = models.CharField(max_length=15)
    type = models.CharField(max_length=15)

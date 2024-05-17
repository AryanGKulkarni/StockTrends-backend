from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class StockSymbol(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=15, default="USD")
    description = models.TextField(default="USD")
    currency = models.CharField(max_length=15, default="USD")
    type = models.CharField(max_length=15, default="USD")

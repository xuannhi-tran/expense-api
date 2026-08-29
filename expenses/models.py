from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Expense(models.Model):
    name = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=50, default='Other')
    user = models.ForeignKey(
        User, 
        on_delete= models.CASCADE
    )
    class Meta: 
        ordering = ['id']

    def __str__(self):
        return self.name
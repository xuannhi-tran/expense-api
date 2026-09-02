from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Expense(models.Model):
    name = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=50)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', '-id']

    def __str__(self):
        return self.name
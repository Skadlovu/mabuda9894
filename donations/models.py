from email.policy import default
from re import M
from unittest.util import _MAX_LENGTH
from django.db import models

class Donation(models.Model):
    amount = models.IntegerField( default=0)
    item_name=models.CharField(max_length=20, default='Donation')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)
    transaction_id=models.CharField(max_length=255)

    def __str__(self):
        return f'Donation #{self.id} - {self.name} ({self.amount})'
    

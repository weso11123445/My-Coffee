from django.db import models
from datetime import datetime
# Create your models here.

class Product(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField(null=True , blank=True)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    photo = models.ImageField(upload_to='photo/%y/%m/%d' ,null=True , blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']

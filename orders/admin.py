from django.contrib import admin
from .models import Order
from .models import OrderDetails
from .models import Payment

# Register your models here.
admin.site.register(Order)
admin.site.register(OrderDetails)
admin.site.register(Payment)

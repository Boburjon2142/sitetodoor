from django.contrib import admin

from .models import Delivery, Order, OrderItem

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Delivery)

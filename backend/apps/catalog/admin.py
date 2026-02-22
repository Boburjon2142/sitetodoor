from django.contrib import admin

from .models import Product, ProductCategory, SupplierOffer, SupplierProfile

admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(SupplierProfile)
admin.site.register(SupplierOffer)

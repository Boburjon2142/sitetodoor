from django.contrib import admin

from .models import (
    Address,
    Cart,
    CartItem,
    Category,
    Complaint,
    CompareItem,
    Favorite,
    NotificationSetting,
    Order,
    OrderItem,
    Product,
    ProductImage,
    RecentlyViewed,
    UserProfile,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "unit", "stock_quantity", "is_available", "is_featured")
    list_filter = ("category", "is_available", "is_featured")
    search_fields = ("name", "sku", "brand")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "phone", "status", "delivery_type", "total_price", "created_at")
    list_filter = ("status", "delivery_type", "created_at")


admin.site.register(UserProfile)
admin.site.register(Address)
admin.site.register(Favorite)
admin.site.register(CompareItem)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(OrderItem)
admin.site.register(Complaint)
admin.site.register(NotificationSetting)
admin.site.register(RecentlyViewed)

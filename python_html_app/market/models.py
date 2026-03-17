from decimal import Decimal

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    UNIT_CHOICES = [
        ("dona", "dona"),
        ("kg", "kg"),
        ("qop", "qop"),
        ("m2", "m2"),
        ("m3", "m3"),
        ("metr", "metr"),
    ]

    name = models.CharField(max_length=180)
    slug = models.SlugField(unique=True, max_length=220)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    brand = models.CharField(max_length=120, blank=True)
    description_short = models.CharField(max_length=255)
    description_full = models.TextField(blank=True)
    technical_specs = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default="dona")
    stock_quantity = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=40, unique=True)
    is_available = models.BooleanField(default=True)
    image = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 2
            while Product.objects.exclude(pk=self.pk).filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        self.is_available = self.stock_quantity > 0
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("product_detail", args=[self.slug])

    @property
    def stock_status(self):
        if self.stock_quantity == 0:
            return "yoq"
        if self.stock_quantity < 10:
            return "kam"
        return "mavjud"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="gallery")
    image_url = models.URLField()
    alt_text = models.CharField(max_length=120, blank=True)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.name} rasmi"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=120, default="Qarshi")
    district = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return self.user.username


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    title = models.CharField(max_length=80)
    full_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30)
    region = models.CharField(max_length=120, default="Qashqadaryo")
    city = models.CharField(max_length=120, default="Qarshi")
    street = models.CharField(max_length=255)
    landmark = models.CharField(max_length=255, blank=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_default", "-created_at"]

    def __str__(self):
        return f"{self.title} - {self.city}"

    def full_address(self):
        bits = [self.region, self.city, self.street]
        if self.landmark:
            bits.append(self.landmark)
        return ", ".join(bits)


class SessionOwnedModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Favorite(SessionOwnedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="favorited_by")

    class Meta:
        ordering = ["-created_at"]


class CompareItem(SessionOwnedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="compared_by")

    class Meta:
        ordering = ["created_at"]


class Cart(SessionOwnedModel):
    def __str__(self):
        return f"Cart {self.pk}"

    @property
    def subtotal(self):
        return sum(item.line_total for item in self.items.select_related("product"))


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("cart", "product")

    @property
    def line_total(self):
        return self.product.price * self.quantity


class Order(models.Model):
    STATUS_CHOICES = [
        ("yangi", "Yangi"),
        ("qabul_qilindi", "Qabul qilindi"),
        ("yolda", "Yo'lda"),
        ("yakunlandi", "Yakunlandi"),
        ("bekor_qilingan", "Bekor qilingan"),
    ]
    DELIVERY_CHOICES = [
        ("tezkor", "Tezkor yetkazish"),
        ("oddiy", "Oddiy yetkazish"),
        ("olib_ketish", "Olib ketish"),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")
    full_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")
    address_text = models.TextField()
    delivery_type = models.CharField(max_length=20, choices=DELIVERY_CHOICES, default="oddiy")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="yangi")
    note = models.TextField(blank=True)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Buyurtma #{self.pk}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.CharField(max_length=180)
    unit = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    line_total = models.DecimalField(max_digits=12, decimal_places=2)


class Complaint(models.Model):
    STATUS_CHOICES = [
        ("yangi", "Yangi"),
        ("korib_chiqilmoqda", "Ko'rib chiqilmoqda"),
        ("hal_qilindi", "Hal qilindi"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="complaints")
    subject = models.CharField(max_length=180)
    message = models.TextField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="yangi")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class NotificationSetting(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="notification_settings")
    order_updates = models.BooleanField(default=True)
    promo_news = models.BooleanField(default=True)
    system_alerts = models.BooleanField(default=True)


class RecentlyViewed(SessionOwnedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="views")

    class Meta:
        ordering = ["-created_at"]

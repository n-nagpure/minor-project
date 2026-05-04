import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class AccountProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="account_profile")
    email_verified = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.user.username} verified={self.email_verified}"


class EmailVerificationToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="email_verification_tokens")
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.user_id} {self.token}"


class Product(models.Model):
    name = models.CharField(max_length=255)
    model_number = models.CharField(max_length=120, unique=True)
    brand = models.CharField(max_length=120, blank=True)
    image_url = models.URLField(blank=True)
    category = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.model_number})"


class ProductPrice(models.Model):
    WEBSITE_CHOICES = [
        ("amazon", "Amazon"),
        ("flipkart", "Flipkart"),
        ("croma", "Croma"),
        ("reliance", "Reliance Digital"),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="prices")
    source = models.CharField(max_length=40, choices=WEBSITE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    buy_url = models.URLField()
    in_stock = models.BooleanField(default=True)
    fetched_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("product", "source")

    def __str__(self) -> str:
        return f"{self.product.model_number} - {self.source}: {self.price}"


class WishlistItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wishlist_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="wishlisted_by")
    target_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notify_on_drop = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "product")

    def __str__(self) -> str:
        return f"{self.user.username} - {self.product.model_number}"


class ProductListing(models.Model):
    PLATFORM_CHOICES = [
        ("amazon", "Amazon"),
        ("flipkart", "Flipkart"),
        ("croma", "Croma"),
        ("reliance", "Reliance Digital"),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="listings")
    platform = models.CharField(max_length=40, choices=PLATFORM_CHOICES)
    platform_product_id = models.CharField(max_length=150, blank=True)
    title = models.CharField(max_length=300)
    buy_url = models.URLField()
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    fetched_at = models.DateTimeField(auto_now=True)
    last_success_at = models.DateTimeField(null=True, blank=True)
    last_error = models.TextField(blank=True)

    class Meta:
        unique_together = ("product", "platform")
        indexes = [models.Index(fields=["platform", "fetched_at"])]

    def __str__(self) -> str:
        return f"{self.product.model_number} - {self.platform}: {self.current_price}"


class PriceHistory(models.Model):
    listing = models.ForeignKey(ProductListing, on_delete=models.CASCADE, related_name="price_history")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    captured_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["captured_at"])]

    def __str__(self) -> str:
        return f"{self.listing.platform} {self.price} @ {self.captured_at}"

import uuid

from django.db import models
from django.contrib.auth import get_user_model

from products.models import Product


User = get_user_model()


class OrderStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    PAID = "paid", "Paid"
    SHIPPED = "shipped", "Shipped"
    DELIVERED = "delivered", "Delivered"
    CANCELLED = "cancelled", "Cancelled"
    FAILED = "failed", "Failed"
    REFUNDED = "refunded", "Refunded"


class Order(models.Model):

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["-created_at"]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name="orders", on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    stripe_payment_intent_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    shipping_full_name = models.CharField(max_length=100)
    shipping_address_line1 = models.CharField(max_length=255)
    shipping_address_line2 = models.CharField(max_length=255, blank=True)
    shipping_postal_code = models.CharField(max_length=20)
    shipping_city = models.CharField(max_length=100)
    shipping_country = models.CharField(max_length=100)

    billing_full_name = models.CharField(max_length=100)
    billing_address_line1 = models.CharField(max_length=255)
    billing_address_line2 = models.CharField(max_length=255, blank=True)
    billing_postal_code = models.CharField(max_length=20)
    billing_city = models.CharField(max_length=100)
    billing_country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id} — {self.status}"


class OrderItem(models.Model):

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)

    product = models.ForeignKey(Product, related_name="order_items", on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=8, decimal_places=2)

    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product_name}"

    @property
    def subtotal(self):
        return self.product_price * self.quantity

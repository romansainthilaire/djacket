import uuid

from django.db import models, transaction
from django.contrib.auth import get_user_model
from django.utils import timezone

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
        verbose_name = "order"
        verbose_name_plural = "orders"
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
        verbose_name = "order item"
        verbose_name_plural = "order items"

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


class InvoiceSequence(models.Model):

    class Meta:
        verbose_name = "invoice sequence"
        verbose_name_plural = "invoice sequences"
        ordering = ["-year"]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    year = models.PositiveIntegerField(unique=True)
    last_number = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.year} → {self.last_number}"


class Invoice(models.Model):

    class Meta:
        verbose_name = "invoice"
        verbose_name_plural = "invoices"
        ordering = ["-created_at"]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    order = models.OneToOneField(Order, related_name="invoice", on_delete=models.CASCADE)
    number = models.CharField(max_length=20, unique=True, editable=False)

    def __str__(self):
        return self.number

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = self.generate_number()
        super().save(*args, **kwargs)

    def generate_number(self):
        current_year = timezone.now().year
        with transaction.atomic():
            sequence, _ = InvoiceSequence.objects.select_for_update().get_or_create(
                year=current_year,
                defaults={"last_number": 0}
            )
            sequence.last_number += 1
            sequence.save()
            return f"FA{current_year}{sequence.last_number:05d}"

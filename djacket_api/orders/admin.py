from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "stripe_payment_intent_id",
        "items_display",
        "total_amount_display",
        "status",
        "paid_at"
    ]
    list_filter = ["status"]
    search_fields = [
        "stripe_payment_intent_id",
        "user__email",
        "user__username"
    ]

    def items_display(self, obj):
        items = obj.items.all()
        html = ""
        for item in items:
            html += f"<div style='white-space: nowrap;'>{item.quantity} x {item.product_name}</div>"
        return mark_safe(html)
    items_display.short_description = "items"

    def total_amount_display(self, obj):
        return f"{obj.total_amount} €"
    total_amount_display.short_description = "total amount"

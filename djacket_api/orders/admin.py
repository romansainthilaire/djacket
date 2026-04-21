from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Order, InvoiceSequence, Invoice


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


@admin.register(InvoiceSequence)
class InvoiceSequenceAdmin(admin.ModelAdmin):
    list_display = [
        "year",
        "last_number",
        "created_at",
        "updated_at"
    ]
    readonly_fields = [
        "year",
        "last_number",
        "created_at",
        "updated_at"
    ]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = [
        "number",
        "order_id",
        "email",
        "created_at"
    ]
    readonly_fields = [
        "number",
        "order",
        "created_at",
        "updated_at"
    ]
    search_fields = [
        "number",
        "order__id",
        "order__user__email"
    ]
    list_select_related = ["order", "order__user"]

    def order_id(self, obj):
        return obj.order.id
    order_id.short_description = "Order ID"

    def email(self, obj):
        return obj.order.user.email if obj.order.user else "-"
    email.short_description = "Email"

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

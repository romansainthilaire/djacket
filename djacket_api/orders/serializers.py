from rest_framework import serializers

from products.models import Product

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "product_name",
            "product_price",
            "quantity",
            "subtotal"
        ]
        read_only_fields = [
            "product_name",
            "product_price",
            "subtotal"
        ]

    def get_subtotal(self, obj):
        return obj.subtotal

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0.")
        return value


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "items",
            "status",
            "total_amount",
            "paid_at",
            "shipping_full_name",
            "shipping_address_line1",
            "shipping_address_line2",
            "shipping_postal_code",
            "shipping_city",
            "shipping_country",
            "billing_full_name",
            "billing_address_line1",
            "billing_address_line2",
            "billing_postal_code",
            "billing_city",
            "billing_country"
        ]
        read_only_fields = [
            "id",
            "status",
            "total_amount",
            "paid_at"
        ]

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError("Order must contain at least one item.")
        return items

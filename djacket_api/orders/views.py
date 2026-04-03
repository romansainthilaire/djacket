import stripe

from django.conf import settings
from django.db import transaction

from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from products.models import Product
from .models import Order, OrderItem
from .serializers import OrderSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY


class OrderViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):

    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    @action(detail=False, methods=["post"], url_path="checkout")
    def checkout(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():

            items = serializer.validated_data["items"]

            total_amount = sum([item["product"].price * item["quantity"] for item in items])

            order = Order.objects.create(
                user=self.request.user,
                total_amount=total_amount,
                shipping_full_name=serializer.validated_data["shipping_full_name"],
                shipping_address_line1=serializer.validated_data["shipping_address_line1"],
                shipping_address_line2=serializer.validated_data["shipping_address_line2"],
                shipping_postal_code=serializer.validated_data["shipping_postal_code"],
                shipping_city=serializer.validated_data["shipping_city"],
                shipping_country=serializer.validated_data["shipping_country"],
                billing_full_name=serializer.validated_data["billing_full_name"],
                billing_address_line1=serializer.validated_data["billing_address_line1"],
                billing_address_line2=serializer.validated_data["billing_address_line2"],
                billing_postal_code=serializer.validated_data["billing_postal_code"],
                billing_city=serializer.validated_data["billing_city"],
                billing_country=serializer.validated_data["billing_country"]
            )

            for item in items:
                product: Product = item["product"]
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    product_name=product.name,
                    product_price=product.price,
                    quantity=item["quantity"]
                )

            stripe_payment_intent = stripe.PaymentIntent.create(
                amount=int(order.total_amount * 100),
                currency="eur",
                metadata={"order_id": str(order.id)},
                automatic_payment_methods={"enabled": True}
            )

            order.stripe_payment_intent_id = stripe_payment_intent["id"]
            order.save()

        return Response(
            {
                "order": OrderSerializer(order).data,
                "client_secret": stripe_payment_intent["client_secret"]
            },
            status=status.HTTP_201_CREATED
        )

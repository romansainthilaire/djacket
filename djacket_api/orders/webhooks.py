import stripe
import logging
import uuid

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from .models import Order, OrderStatus

stripe.api_key = settings.STRIPE_SECRET_KEY


def is_valid_uuid(value):
    try:
        uuid.UUID(str(value))
        return True
    except ValueError:
        return False


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        logging.error(f"Stripe webhook - invalid payload: {e}")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        logging.error(f"Stripe webhook - invalid signature: {e}")
        return HttpResponse(status=400)

    if event["type"] not in [
        "payment_intent.succeeded",
        "payment_intent.payment_failed",
        "payment_intent.canceled"
    ]:
        logging.info(f"Stripe webhook - unhandled event type: {event['type']}")
        return HttpResponse(status=200)  # status 200 to prevent retries

    payment_intent = event["data"]["object"]
    order_id = payment_intent["metadata"].get("order_id")

    if not order_id:
        logging.error("Stripe webhook - missing order_id in metadata.")
        return HttpResponse(status=200)  # status 200 to prevent retries

    if not is_valid_uuid(order_id):
        logging.error(f"Stripe webhook - invalid order_id format: {order_id}")
        return HttpResponse(status=200)  # status 200 to prevent retries

    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        logging.error(f"Stripe webhook - order not found: {order_id}")
        return HttpResponse(status=200)  # status 200 to prevent retries

    if order.status == OrderStatus.PAID:
        logging.info(f"Stripe webhook - order already paid: {order_id}")
        return HttpResponse(status=200)  # status 200 to prevent retries

    if event["type"] == "payment_intent.succeeded":
        order.status = OrderStatus.PAID
        order.paid_at = timezone.now()
        order.save()

    elif event["type"] == "payment_intent.payment_failed":
        if order.status == OrderStatus.PENDING:
            order.status = OrderStatus.FAILED
            order.save()

    elif event["type"] == "payment_intent.canceled":
        if order.status == OrderStatus.PENDING:
            order.status = OrderStatus.CANCELLED
            order.save()

    return HttpResponse(status=200)

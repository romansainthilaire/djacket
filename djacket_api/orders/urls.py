from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import OrderViewSet, InvoiceViewSet, invoice_html
from .webhooks import stripe_webhook

router = DefaultRouter()
router.register("orders", OrderViewSet, basename="order")
router.register("invoices", InvoiceViewSet, basename="invoice")

urlpatterns = [
    path("stripe/webhook/", stripe_webhook, name="stripe-webhook"),
    path("invoice-html/<str:signed_invoice_id>/", invoice_html, name="invoice-html"),
    path("", include(router.urls))
]

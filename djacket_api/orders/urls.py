from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import OrderViewSet
from .webhooks import stripe_webhook

router = DefaultRouter()
router.register("orders", OrderViewSet, basename="order")

urlpatterns = [
    path("stripe/webhook/", stripe_webhook, name="stripe-webhook"),
    path("", include(router.urls))
]

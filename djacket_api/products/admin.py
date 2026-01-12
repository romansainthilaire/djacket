from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ["name"]
    search_fields = ["name"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ["name", "price_euros", "category"]
    list_filter = ["category"]
    search_fields = ["name"]

    def price_euros(self, obj):
        return f"{obj.price} €".replace(".", ",")
    price_euros.short_description = "Price"

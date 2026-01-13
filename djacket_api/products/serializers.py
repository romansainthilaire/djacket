from rest_framework import serializers

from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            "id",
            "name"
        ]


class ProductListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "name",
            "price",
            "thumbnail"
        ]


class ProductDetailSerializer(serializers.ModelSerializer):

    category = CategorySerializer()

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "name",
            "description",
            "price",
            "image"
        ]

from rest_framework import serializers

from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            "name",
            "slug"
        ]


class ProductListSerializer(serializers.ModelSerializer):

    category_slug = serializers.SlugRelatedField(
        source="category",
        slug_field="slug",
        read_only=True
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "category_slug",
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

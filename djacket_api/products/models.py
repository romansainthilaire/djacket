import os
from io import BytesIO
from PIL import Image

from django.db import models
from django.core.files import File


class Category(models.Model):

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["name"]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to="products/images/", blank=True, null=True)
    thumbnail = models.ImageField(upload_to="products/thumbnails/", blank=True, null=True)

    def __str__(self):
        return self.name

    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img = img.convert("RGB")
        img.thumbnail(size)
        thumb_io = BytesIO()
        img.save(thumb_io, format="JPEG", quality=85)
        thumbnail = File(thumb_io, name=os.path.basename(image.name))
        return thumbnail

    def save(self, *args, **kwargs):
        if self.image:
            self.thumbnail = self.make_thumbnail(self.image)
        super().save(*args, **kwargs)

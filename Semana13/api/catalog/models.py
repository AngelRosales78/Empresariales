from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Category(models.Model):
    name = models.CharField("nombre", max_length=80, unique=True)
    description = models.TextField("descripción", blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "categoría"
        verbose_name_plural = "categorías"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="categoría",
    )
    name = models.CharField("nombre", max_length=120)
    description = models.TextField("descripción", blank=True)
    price = models.DecimalField(
        "precio",
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    stock = models.PositiveIntegerField("existencias", default=0)
    image = models.ImageField("imagen", upload_to="products/", blank=True)
    created_at = models.DateTimeField("fecha de alta", auto_now_add=True)

    class Meta:
        ordering = ["name", "id"]
        verbose_name = "producto"
        verbose_name_plural = "productos"

    def __str__(self):
        return self.name

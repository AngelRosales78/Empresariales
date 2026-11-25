from django.contrib import admin
from django.db.models import Count

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "product_count"]
    search_fields = ["name", "description"]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(total_products=Count("products"))

    @admin.display(description="productos", ordering="total_products")
    def product_count(self, category):
        return category.total_products


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "price", "stock", "created_at"]
    list_filter = ["category", "created_at"]
    list_editable = ["price", "stock"]
    list_select_related = ["category"]
    search_fields = ["name", "description"]

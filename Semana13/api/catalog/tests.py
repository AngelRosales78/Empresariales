import shutil
import tempfile

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import override_settings
from rest_framework.test import APITestCase

from .management.commands.seed_catalog import build_image
from .models import Category, Product


class CatalogApiTests(APITestCase):
    def setUp(self):
        media = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, media, ignore_errors=True)
        override = override_settings(MEDIA_ROOT=media)
        override.enable()
        self.addCleanup(override.disable)
        call_command("seed_catalog", verbosity=0)
        self.category = Category.objects.get(name="Ropa")
        self.staff = User.objects.create_user("staff", is_staff=True)

    def payload(self, **changes):
        return {
            "name": "Casaca", "description": "Abrigo", "price": "99.90",
            "stock": 3, "category_id": self.category.id, **changes,
        }

    def test_seed_is_idempotent_and_every_product_has_image(self):
        call_command("seed_catalog", verbosity=0)
        self.assertEqual((Category.objects.count(), Product.objects.count()), (3, 9))
        self.assertFalse(Product.objects.filter(image="").exists())

    def test_list_nests_category_in_one_query(self):
        with self.assertNumQueries(1):
            response = self.client.get("/api/products/")
        self.assertEqual(len(response.data), 9)
        self.assertEqual(set(response.data[0]["category"]), {"id", "name", "description"})

    def test_filters_by_category(self):
        response = self.client.get("/api/products/", {"category": self.category.id})
        self.assertEqual({p["category"]["name"] for p in response.data}, {"Ropa"})
        self.assertEqual(self.client.get("/api/products/?category=x").status_code, 400)

    def test_anonymous_cannot_write(self):
        self.assertEqual(self.client.post("/api/products/", self.payload()).status_code, 401)

    def test_staff_creates_with_image_and_gets_nested_category(self):
        self.client.force_authenticate(self.staff)
        image = SimpleUploadedFile("new.png", build_image("mug", "#000000").read(), "image/png")
        response = self.client.post("/api/products/", self.payload(image=image), format="multipart")
        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(response.data["category"]["name"], "Ropa")
        self.assertTrue(response.data["image"])

    def test_staff_updates_and_keeps_image(self):
        self.client.force_authenticate(self.staff)
        product = Product.objects.first()
        response = self.client.patch(
            f"/api/products/{product.id}/", self.payload(), format="multipart"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Casaca")
        self.assertTrue(response.data["image"])

    def test_staff_deletes(self):
        self.client.force_authenticate(self.staff)
        product = Product.objects.first()
        self.assertEqual(self.client.delete(f"/api/products/{product.id}/").status_code, 204)
        self.assertFalse(Product.objects.filter(pk=product.pk).exists())

    def test_rejects_invalid_values(self):
        self.client.force_authenticate(self.staff)
        for field, value in (("price", "0"), ("stock", -1), ("category_id", 9999), ("name", "")):
            with self.subTest(field=field):
                response = self.client.post("/api/products/", self.payload(**{field: value}))
                self.assertEqual(response.status_code, 400)
                self.assertIn(field, response.data)

    def test_category_with_products_is_protected(self):
        self.client.force_authenticate(self.staff)
        response = self.client.delete(f"/api/categories/{self.category.id}/")
        self.assertEqual(response.status_code, 409)

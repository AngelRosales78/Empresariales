from io import BytesIO

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify
from PIL import Image, ImageDraw

from catalog.models import Category, Product
from catalog.seed_data import CATALOG

LIGHT = "#f6efe0"
ACCENT = "#e8b04b"


def draw_shape(draw, shape, color):
    if shape == "poster":
        draw.rectangle((200, 90, 440, 430), fill=LIGHT)
        draw.ellipse((250, 150, 390, 290), fill=ACCENT)
        draw.rectangle((230, 340, 410, 355), fill=color)
        draw.rectangle((230, 375, 350, 390), fill=color)
    elif shape == "cards":
        for offset, fill in ((0, "#d9cba8"), (45, ACCENT), (90, LIGHT)):
            draw.rectangle((140 + offset, 130 + offset, 400 + offset, 300 + offset), fill=fill)
    elif shape == "shirt":
        draw.polygon([(240, 110), (400, 110), (510, 190), (460, 260), (420, 230), (420, 430),
                      (220, 430), (220, 230), (180, 260), (130, 190)], fill=LIGHT)
        draw.pieslice((270, 60, 370, 160), 0, 180, fill=color)
        draw.ellipse((280, 230, 360, 310), fill=ACCENT)
    elif shape == "cap":
        draw.pieslice((170, 130, 450, 450), 180, 360, fill=LIGHT)
        draw.rounded_rectangle((170, 285, 560, 325), 20, fill=ACCENT)
    elif shape == "bag":
        draw.arc((240, 70, 400, 330), 180, 360, fill=LIGHT, width=18)
        draw.polygon([(190, 200), (450, 200), (480, 430), (160, 430)], fill=LIGHT)
        draw.ellipse((275, 265, 365, 355), fill=ACCENT)
    elif shape == "mug":
        draw.ellipse((380, 190, 510, 350), outline=LIGHT, width=26)
        draw.rounded_rectangle((170, 130, 420, 410), 28, fill=LIGHT)
        draw.rectangle((170, 240, 420, 300), fill=ACCENT)
    elif shape == "bucket":
        for x in range(190, 430, 50):
            draw.ellipse((x, 90, x + 80, 210), fill=ACCENT)
        draw.polygon([(170, 170), (470, 170), (420, 430), (220, 430)], fill=LIGHT)
        for x in (235, 355):
            draw.polygon([(x - 15, 170), (x + 45, 170), (x + 40, 430), (x, 430)], fill=color)
    elif shape == "cushion":
        draw.rounded_rectangle((170, 110, 470, 410), 60, fill=LIGHT)
        draw.rounded_rectangle((215, 155, 425, 365), 40, outline=ACCENT, width=14)


def build_image(shape, color):
    image = Image.new("RGB", (640, 520), color)
    draw_shape(ImageDraw.Draw(image), shape, color)
    buffer = BytesIO()
    image.save(buffer, "PNG")
    return ContentFile(buffer.getvalue())


class Command(BaseCommand):
    help = "Carga las categorías y los productos con imagen. Repetirlo no duplica datos."

    @transaction.atomic
    def handle(self, *args, **options):
        for category_name, category_description, color, products in CATALOG:
            category, _ = Category.objects.get_or_create(
                name=category_name, defaults={"description": category_description}
            )
            for name, description, price, stock, shape in products:
                product, _ = Product.objects.get_or_create(
                    name=name,
                    category=category,
                    defaults={"description": description, "price": price, "stock": stock},
                )
                if not product.image:
                    product.image.save(f"{slugify(name)}.png", build_image(shape, color))
        if options["verbosity"] > 0:
            self.stdout.write(self.style.SUCCESS(
                f"Listo: {Category.objects.count()} categorías, {Product.objects.count()} productos."
            ))

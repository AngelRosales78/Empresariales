import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.utils import timezone
from datetime import timedelta
from appnews.models import Category, Author, Article
from PIL import Image
import os

os.makedirs("media/articles", exist_ok=True)
os.makedirs("media/avatars", exist_ok=True)

for i in range(1, 4):
    img = Image.new("RGB", (800, 400), color=(26, 35, 126 + i * 30))
    img.save(f"media/articles/article_{i}.jpg")

for i in range(1, 3):
    img = Image.new("RGB", (200, 200), color=(40, 53, 147 + i * 20))
    img.save(f"media/avatars/avatar_{i}.jpg")

now = timezone.now()

c1, _ = Category.objects.get_or_create(name="Tecnologia", slug="tecnologia")
c2, _ = Category.objects.get_or_create(name="Deportes", slug="deportes")
c3, _ = Category.objects.get_or_create(name="Economia", slug="economia")

a1, _ = Author.objects.get_or_create(
    name="Juan Perez",
    defaults={
        "email": "juan@example.com",
        "bio": "Periodista tecnol\u00f3gico",
    },
)
a2, _ = Author.objects.get_or_create(
    name="Maria Garcia",
    defaults={
        "email": "maria@example.com",
        "bio": "Corresponsal deportiva",
    },
)

articles_data = [
    {
        "title": "Inteligencia Artificial revoluciona la industria en 2026",
        "slug": "ia-revoluciona-2026",
        "summary": "Las empresas adoptan modelos de IA generativa para transformar sus procesos productivos y mejorar la experiencia del cliente.",
        "content": "La inteligencia artificial est\u00e1 transformando radicalmente la forma en que las empresas operan. Desde modelos de lenguaje hasta sistemas de visi\u00f3n por computadora, las aplicaciones son cada vez m\u00e1s diversas. Expertos sealan que el a\u00f1o 2026 ser\u00e1 un punto de inflexi\u00f3n en la adopci\u00f3n masiva de estas tecnolog\u00edas.",
        "author": a1,
        "category": c1,
        "image": "articles/article_1.jpg",
        "days_ago": 5,
    },
    {
        "title": "Nuevo avance en computaci\u00f3n cu\u00e1ntica promete cambios",
        "slug": "computacion-cuantica-avance",
        "summary": "Investigadores logran un hito en estabilidad de qubits que podr\u00eda acelerar la computaci\u00f3n cu\u00e1ntica comercial.",
        "content": "Un equipo internacional de investigadores ha logrado un avance significativo en la estabilidad de los qubits, los componentes b\u00e1sicos de las computadoras cu\u00e1nticas. Este progreso podr\u00eda acelerar la llegada de computadoras cu\u00e1nticas comerciales capaces de resolver problemas que hoy son inalcanzables para los supercomputadores cl\u00e1sicos.",
        "author": a1,
        "category": c1,
        "image": "articles/article_2.jpg",
        "days_ago": 10,
    },
    {
        "title": "La selecci\u00f3n nacional clasifica al mundial",
        "slug": "seleccion-clasifica-mundial",
        "summary": "Con un triunfo contundente, el equipo nacional asegura su place en el pr\u00f3ximo campeonato mundial de f\u00fatbol.",
        "content": "La selecci\u00f3n nacional logr\u00f3 una clasificaci\u00f3n hist\u00f3rica al vencer por 3-0 en el partido decisivo. Los goles fueron obra de un tr\u00edo ofensivo que ha sido la clave del torneo. La celebraci\u00f3n se extendi\u00f3 por todo el pa\u00eds mientras miles de aficionados salieron a las calles a celebrar.",
        "author": a2,
        "category": c2,
        "image": "articles/article_3.jpg",
        "days_ago": 3,
    },
    {
        "title": "Maratona de Tokio establece nuevo r\u00e9cord mundial",
        "slug": "maratona-tokio-record",
        "summary": "El keniano rompe la barrera de las 2 horas en el marat\u00f3n m\u00e1s competitivo del a\u00f1o.",
        "content": "En una actuaci\u00f3n que fue calificada como una de las m\u00e1s impresionantes en la historia del atletismo, el corredor keniano rompi\u00f3 la barrera de las 2 horas en el marat\u00f3n de Tokio. El tiempo de 1:59:32 super\u00f3 el r\u00e9cord anterior en m\u00e1s de 10 segundos, un margen colossal en este deporte.",
        "author": a2,
        "category": c2,
        "image": "articles/article_3.jpg",
        "days_ago": 15,
    },
    {
        "title": "Los mercados emergentes lideran el crecimiento global",
        "slug": "mercados-emergentes-crecimiento",
        "summary": "Las econom\u00edas en desarrollo muestran se\u00f1ales s\u00f3lidas de expansi\u00f3n mientras los pa\u00edses desarrollados moderan.",
        "content": "Los mercados emergentes est\u00e1n demostrando una resiliencia impresionante en medio de la incertidumbre econ\u00f3mica global. Pa\u00edses como India, Brasil y Vietnam han logrado tasas de crecimiento superiores al 6%, impulsadas por el consumo interno y las reformas estructurales implementadas en los \u00faltimos a\u00f1os.",
        "author": a1,
        "category": c3,
        "image": "articles/article_1.jpg",
        "days_ago": 7,
    },
    {
        "title": "Criptomonedas: regulaci\u00f3n global avanza en el G20",
        "slug": "criptomonedas-regulacion-g20",
        "summary": "L\u00edderes del G20 acuerdan un marco regulatorio compartido para activos digitales y stablecoins.",
        "content": "En una cumbre hist\u00f3rica, los l\u00edderes del G20 acordaron establecer un marco regulatorio global para las criptomonedas y los activos digitales. El acuerdo incluye est\u00e1ndares comunes para stablecoins, exchanges y protocolos DeFi, marcando un antes y un despu\u00e9s en la regulaci\u00f3n de estos activos financieros.",
        "author": a2,
        "category": c3,
        "image": "articles/article_2.jpg",
        "days_ago": 20,
    },
]

for data in articles_data:
    Article.objects.get_or_create(
        slug=data["slug"],
        defaults={
            "title": data["title"],
            "summary": data["summary"],
            "content": data["content"],
            "author": data["author"],
            "category": data["category"],
            "featured_image": data["image"],
            "published_at": now - timedelta(days=data["days_ago"]),
            "is_active": True,
        },
    )

print("6 articles created successfully!")
for a in Article.objects.all():
    print(f"  - {a.title} ({a.category.name})")

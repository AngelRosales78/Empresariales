# Laboratorio 6 — Portal de noticias

Proyecto Django con seis noticias ficticias de demostración, tres categorías y dos autores.

## Ejecutar

Desde esta carpeta:

```powershell
python -m pip install -r requirements.txt
python manage.py migrate
python seed_data.py
python manage.py createsuperuser
python manage.py runserver
```

Portal: http://127.0.0.1:8000/
Administrador: http://127.0.0.1:8000/admin/


## Los doce procedimientos

1. Proyecto `config`, aplicación `news` declarada en INSTALLED_APPS y Pillow en requirements.txt. La etiqueta interna `appnews` conserva la identidad de la migración original; la carpeta y el módulo son `news`.
2. settings.py configura templates, static y media; config/urls.py sirve media cuando DEBUG está activo.
3. news/models.py define Article, Category y Author, imagen destacada, fecha, autor y categorías. Migraciones incluidas; ejecutar migrate y createsuperuser como se indica arriba.
4. templates/base.html define title, content y sidebar.
5. templates/_article_card.html se incluye desde home.html y category_detail.html.
6. home.html usa for/empty; la tarjeta aplica date y truncatewords al resumen.
7. article_detail.html hereda de base e incluye imagen, autor y categorías.
8. category_detail.html reutiliza la tarjeta y muestra el caso vacío.
9. news/urls.py declara home, article_detail y category_detail. Los enlaces de las plantillas utilizan la etiqueta url con el espacio de nombres appnews.
10. base.html usa load static para la hoja de estilos. Las imágenes se cargan de media. CSS y seis imágenes comprobados mediante respuestas HTTP correctas.
11. news/admin.py configura list_display, list_filter y search_fields en las tres entidades. Hay seis noticias en Tecnología, Deportes y Economía (dos por categoría), visibles en la portada.
12. En la noticia “Inteligencia Artificial revoluciona la industria en 2026” se guardó `<strong>Prueba de HTML del laboratorio 6</strong>` dentro del cuerpo.

## Resultado de la prueba de escapado

En el detalle se ve literalmente `<strong>Prueba de HTML del laboratorio 6</strong>`, incluyendo las etiquetas; ese texto no se presenta en negrita. Django escapa los caracteres del contenido: el HTML de respuesta contiene `&lt;strong&gt;Prueba de HTML del laboratorio 6&lt;/strong&gt;`. El filtro linebreaks conserva el escapado automático y añade los párrafos. No se usa safe ni se desactiva autoescape.

## Comprobaciones

Se ejecutaron check y makemigrations --check --dry-run sin incidencias. Se comprobaron las tres páginas, los seis detalles, las categorías, las respuestas sin resultados, el CSS, las imágenes, la configuración administrativa y el escapado. La portada no limita las noticias a los últimos treinta días, por lo que los ejemplos permanecen visibles.


La base de datos y las credenciales locales se omiten del repositorio. Los comandos anteriores crean la base, cargan las seis noticias con sus imágenes y permiten elegir las credenciales del administrador.

Para mantener las sesiones entre reinicios, define DJANGO_SECRET_KEY con una clave propia. Si no está definida, el proyecto genera una clave temporal para desarrollo al arrancar.

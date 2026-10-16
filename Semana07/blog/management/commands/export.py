from django.core.management.base import BaseCommand
from django.core import serializers
from django.contrib.auth.models import User, Group
from blog.models import Author, Post, Comment, Category, Tag, Profile


class Command(BaseCommand):
    help = "Exporta datos de usuarios, grupos y posts a formato JSON."

    def add_arguments(self, parser):
        parser.add_argument(
            "--output", "-o",
            type=str,
            default=None,
            help="Ruta del archivo de salida (por defecto: stdout)",
        )

    def handle(self, *args, **options):
        output = options["output"]

        users_data = serializers.serialize("json", User.objects.all())
        groups_data = serializers.serialize("json", Group.objects.all())
        authors_data = serializers.serialize("json", Author.objects.all())
        categories_data = serializers.serialize("json", Category.objects.all())
        tags_data = serializers.serialize("json", Tag.objects.all())
        posts_data = serializers.serialize(
            "json",
            Post.objects.select_related("author", "category").prefetch_related("tags").all(),
        )
        comments_data = serializers.serialize(
            "json",
            Comment.objects.select_related("post").all(),
        )

        export = {
            "users": users_data,
            "groups": groups_data,
            "authors": authors_data,
            "categories": categories_data,
            "tags": tags_data,
            "posts": posts_data,
            "comments": comments_data,
        }

        import json

        formatted = json.dumps(export, indent=2, ensure_ascii=False)

        if output:
            with open(output, "w", encoding="utf-8") as f:
                f.write(formatted)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Export completado: {output} "
                    f"({User.objects.count()} usuarios, {Group.objects.count()} grupos, "
                    f"{Author.objects.count()} autores, {Post.objects.count()} posts)"
                )
            )
        else:
            self.stdout.write(formatted)

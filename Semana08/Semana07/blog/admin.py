from django.contrib import admin
from django.contrib.auth.models import Group

from blog.models import Author, Category, Comment, Post, Profile, Tag

admin.site.unregister(Group)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("author", "country")
    search_fields = ("author__name", "country")


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "published", "published_at")
    list_filter = ("published", "category", "tags")
    search_fields = ("title", "body")
    raw_id_fields = ("author",)
    filter_horizontal = ("tags",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author_name", "post", "created_at")
    list_filter = ("created_at",)
    search_fields = ("author_name", "text")
    raw_id_fields = ("post",)


@admin.register(Group)
class GroupAdminCustom(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    filter_horizontal = ("permissions",)

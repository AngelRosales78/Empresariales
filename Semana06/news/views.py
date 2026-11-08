from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from .models import Article, Category


def home(request):
    articles = Article.objects.filter(is_active=True).select_related('author', 'category').prefetch_related('categories')
    return render(request, 'home.html', {'articles': articles, 'categories': Category.objects.all()})


def article_detail(request, slug):
    article = get_object_or_404(Article.objects.select_related('author', 'category').prefetch_related('categories'), slug=slug, is_active=True)
    return render(request, 'article_detail.html', {'article': article, 'categories': Category.objects.all()})


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles = Article.objects.filter(Q(category=category) | Q(categories=category), is_active=True).select_related('author', 'category').prefetch_related('categories').distinct()
    return render(request, 'category_detail.html', {'category': category, 'articles': articles, 'categories': Category.objects.all()})

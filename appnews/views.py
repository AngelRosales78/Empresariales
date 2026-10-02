from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .models import Article, Category


def home(request):
    now = timezone.now()
    thirty_days_ago = now - timedelta(days=30)
    articles = Article.objects.filter(
        is_active=True,
        published_at__gte=thirty_days_ago
    ).select_related('author', 'category').prefetch_related('categories')[:6]
    categories = Category.objects.all()
    return render(request, 'home.html', {
        'articles': articles,
        'categories': categories,
    })


def article_detail(request, slug):
    article = get_object_or_404(
        Article,
        slug=slug,
        is_active=True
    )
    article.categories.all()
    categories = Category.objects.all()
    return render(request, 'article_detail.html', {
        'article': article,
        'categories': categories,
    })


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles = Article.objects.filter(
        category=category,
        is_active=True
    ).select_related('author', 'category')
    return render(request, 'category_detail.html', {
        'category': category,
        'articles': articles,
    })

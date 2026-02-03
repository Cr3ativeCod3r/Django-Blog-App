from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Post, Category


class PostSitemap(Sitemap):
    """Sitemap for published posts"""
    changefreq = 'weekly'
    priority = 0.8
    protocol = 'https'
    
    def items(self):
        return Post.objects.filter(published=True).select_related('category')
    
    def lastmod(self, obj):
        return obj.created_at
    
    def location(self, obj):
        return obj.get_url()


class CategorySitemap(Sitemap):
    """Sitemap for categories"""
    changefreq = 'monthly'
    priority = 0.6
    protocol = 'https'
    
    def items(self):
        return Category.objects.all()
    
    def location(self, obj):
        return reverse('category_detail', args=[obj.slug])

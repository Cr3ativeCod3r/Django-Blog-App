from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticPagesSitemap(Sitemap):
    """Sitemap for static pages"""
    changefreq = 'monthly'
    priority = 0.7
    protocol = 'https'
    
    def items(self):
        return [
            'home',
            'about',
            'contact',
            'search',
            'mapa',
            'mozg',
            'statut',
            'foundation',
            'category_list',
        ]
    
    def location(self, item):
        return reverse(item)

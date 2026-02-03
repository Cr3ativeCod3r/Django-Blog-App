from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from apps.posts.models import Post, Category


class CategoryListView(ListView):
    """List all categories"""
    model = Category
    template_name = 'categories/index.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        return Category.objects.all().order_by('name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # SEO Context - to jest LISTA kategorii, nie pojedyncza kategoria
        meta_title = 'Kategorie - Fundacja Chorób Mózgu'
        meta_description = 'Przeglądaj wszystkie kategorie artykułów o chorobach neurologicznych. Znajdź interesujące Cię tematy.'
        
        context.update({
            # Basic Meta
            'meta_title': meta_title,
            'meta_description': meta_description,
            'meta_keywords': 'kategorie, choroby mózgu, neurologia, artykuły medyczne',
            'canonical_url': self.request.build_absolute_uri(),
            
            # Open Graph
            'og_type': 'website',
            'og_title': meta_title,
            'og_description': meta_description,
            'og_url': self.request.build_absolute_uri(),
            'og_image': '/static/images/og-default.jpg',
            
            # Twitter Card
            'twitter_title': meta_title,
            'twitter_description': meta_description,
        })
        
        return context  


class CategoryDetailView(ListView):
    """Display posts from a specific category with pagination"""
    model = Post
    template_name = 'categories/detail.html'
    context_object_name = 'posts'
    paginate_by = 3
    
    def get_queryset(self):
        self.category = get_object_or_404(
            Category, 
            slug=self.kwargs['slug']
        )
        return Post.objects.filter(
            category=self.category,
            published=True
        ).select_related(
            'category', 'author'
        ).prefetch_related(
            'tags'
        ).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        
        # SEO Context dla pojedynczej kategorii
        meta_title = f'{self.category.name} - Fundacja Chorób Mózgu'
        meta_description = f'Artykuły i informacje na temat {self.category.name.lower()}. Dowiedz się więcej o {self.category.name.lower()} i znajdź pomoc.'
        
        context.update({
            # Basic Meta
            'meta_title': meta_title,
            'meta_description': meta_description,
            'meta_keywords': f'{self.category.name.lower()}, choroby mózgu, neurologia',
            'canonical_url': self.request.build_absolute_uri(),
            
            # Open Graph
            'og_type': 'website',
            'og_title': meta_title,
            'og_description': meta_description,
            'og_url': self.request.build_absolute_uri(),
            'og_image': '/static/images/og-default.jpg',
            
            # Twitter Card
            'twitter_title': meta_title,
            'twitter_description': meta_description,
        })
        
        return context
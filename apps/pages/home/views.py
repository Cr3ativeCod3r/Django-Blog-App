from django.views.generic import TemplateView
from apps.posts.models import Post
from apps.banners.models import Banner


class HomeView(TemplateView):
    """
    Home page - post list with layout:
    - Featured posts (first 6)
    - Newest posts (next 5)
    - All posts (next 12)
    """
    template_name = 'home/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        all_posts = Post.objects.filter(
            published=True
        ).select_related(
            'category', 'author'
        ).prefetch_related(
            'tags'
        ).order_by('-created_at')
        
        # First 6 posts are featured
        context['featured_posts'] = all_posts[:6]
        
        # Next 5 are newest (sidebar)
        context['newest_posts'] = all_posts[6:11]
        
        # Next 12 are all posts grid
        context['all_posts'] = all_posts[10:22]
        
        # Get active banners for home page
        context['banner_1'] = Banner.objects.filter(position='home_banner_1', is_active=True).first()
        context['banner_2'] = Banner.objects.filter(position='home_banner_2', is_active=True).first()
        context['banner_3'] = Banner.objects.filter(position='home_banner_3', is_active=True).first()
        
        # SEO Context
        meta_title = 'Fundacja Chorób Mózgu - Aktualności i Artykuły'
        meta_description = 'Fundacja Chorób Mózgu - najnowsze aktualności, artykuły i informacje o chorobach neurologicznych. Wspieramy edukację i świadomość zdrowotną.'
        
        context.update({
            # Basic Meta
            'meta_title': meta_title,
            'meta_description': meta_description,
            'canonical_url': 'https://chorobymozgu.pl/',
            'meta_keywords': 'fundacja chorób mózgu, choroby neurologiczne, zdrowie, edukacja zdrowotna',
            
            # Open Graph
            'og_type': 'website',
            'og_title': meta_title,
            'og_description': meta_description,
            'og_url': 'https://chorobymozgu.pl/',
            'og_image': '/static/images/og-default.jpg',
            
            # Twitter Card
            'twitter_title': meta_title,
            'twitter_description': meta_description,
        })
        
        return context
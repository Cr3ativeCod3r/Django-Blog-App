from django.views.generic import TemplateView, ListView
from django.shortcuts import get_object_or_404
from apps.posts.models import Post, Category
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
        
        return context


class AboutView(TemplateView):
    """About us page"""
    template_name = 'about/index.html'


class ContactView(TemplateView):
    """Contact page"""
    template_name = 'contact/index.html'


class SearchView(TemplateView):
    """Search articles page"""
    template_name = 'search/index.html'


class MozgView(TemplateView):
    """Brain page"""
    template_name = 'mozg/index.html'


class StatutView(TemplateView):
    """Statute page"""
    template_name = 'statut/index.html'


class CategoryListView(ListView):
    """List all categories"""
    model = Category
    template_name = 'categories/index.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        return Category.objects.all().order_by('name')


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
        return context

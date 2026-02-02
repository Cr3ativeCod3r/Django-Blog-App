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

from django.views.generic import TemplateView
from apps.posts.models import Post


class SearchView(TemplateView):
    """Search articles page with smart search"""
    template_name = 'search/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        query = self.request.GET.get('q', '').strip()
        search_type = self.request.GET.get('search_type', 'title_content')  # default: title_content or tags
        
        context['query'] = query
        context['search_type'] = search_type
        context['results'] = []
        context['search_performed'] = False
        context['fallback_used'] = False
        
        if query:
            context['search_performed'] = True
            
            if search_type == 'title_content':
                # First, search by title
                results = Post.objects.filter(
                    title__icontains=query,
                    published=True
                ).select_related('category', 'author').prefetch_related('tags').order_by('-created_at')
                
                # If nothing found in title, search in content
                if not results.exists():
                    context['fallback_used'] = True
                    results = Post.objects.filter(
                        content__icontains=query,
                        published=True
                    ).select_related('category', 'author').prefetch_related('tags').order_by('-created_at')
                
                context['results'] = results
                
            elif search_type == 'tags':
                # Search by tags
                results = Post.objects.filter(
                    tags__name__icontains=query,
                    published=True
                ).distinct().select_related('category', 'author').prefetch_related('tags').order_by('-created_at')
                
                context['results'] = results
        
        return context

from django.views.generic import TemplateView


class StatutView(TemplateView):
    """Statute page"""
    template_name = 'statut/index.html' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # SEO Context
        meta_title = 'Statut Fundacji Chorób Mózgu - Dokumenty prawne'
        meta_description = 'Zapoznaj się ze statutem Fundacji Chorób Mózgu. Poznaj cele fundacji, jej strukturę oraz zasady działania.'
        meta_keywords = 'statut, Fundacja Chorób Mózgu, dokumenty prawne, cele fundacji, struktura fundacji, regulamin'
        canonical_url = self.request.build_absolute_uri()
        
        context.update({
            # Basic Meta
            'meta_title': meta_title,
            'meta_description': meta_description,
            'meta_keywords': meta_keywords,
            'canonical_url': canonical_url,
            
            # Open Graph
            'og_type': 'website',
            'og_title': meta_title,
            'og_description': meta_description,
            'og_url': canonical_url,
            'og_image': '/static/images/og-default.jpg',
            
            # Twitter Card
            'twitter_title': meta_title,
            'twitter_description': meta_description,
            'twitter_image': '/static/images/og-default.jpg',
        })
        
        return context  

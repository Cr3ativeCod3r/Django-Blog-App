from django.views.generic import TemplateView


class AboutView(TemplateView):
    """About us page"""
    template_name = 'about/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # SEO Context
        meta_title = 'O nas - Fundacja Chorób Mózgu'
        meta_description = 'Poznaj historię Fundacji Chorób Mózgu, jej misję oraz założycieli. Dowiedz się więcej o naszej działalności na rzecz pacjentów z chorobami neurologicznymi.'
        
        context.update({
            # Basic Meta
            'meta_title': meta_title,
            'meta_description': meta_description,
            'meta_keywords': 'Fundacja Chorób Mózgu, o nas, historia fundacji, misja, założyciele, Jadwiga Pawłowska-Machajek, Wojciech Machajek',
            'canonical_url': self.request.build_absolute_uri(),  # DODAJ TO
            
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

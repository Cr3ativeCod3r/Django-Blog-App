from django.views.generic import TemplateView


class FoundationView(TemplateView):
    """Foundation page with links to various foundation-related pages"""
    template_name = 'foundation/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['foundation_sections'] = [
            {
                'title': 'O nas',
                'description': 'Poznaj historię i misję Fundacji FCHM',
                'url_name': 'about',
                'icon': 'info'
            },
            {
                'title': 'Statut',
                'description': 'Zapoznaj się ze statutem fundacji',
                'url_name': 'statut',
                'icon': 'document'
            },
            {
                'title': 'Kontakt',
                'description': 'Skontaktuj się z nami',
                'url_name': 'contact',
                'icon': 'mail'
            },
        ]
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # SEO Context
        meta_title = 'Fundacja Chorób Mózgu - O nas'
        meta_description = 'Poznaj historię, misję i wartości Fundacji Chorób Mózgu. Dowiedz się, dlaczego działamy i komu pomagamy.'
        meta_keywords = 'Fundacja Chorób Mózgu, o nas, misja, wizja, wartości, historia, cele, zarząd, rada fundacji'
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
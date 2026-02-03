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

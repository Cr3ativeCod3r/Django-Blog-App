from django.views.generic import TemplateView


class StatutView(TemplateView):
    """Statute page"""
    template_name = 'statut/index.html'

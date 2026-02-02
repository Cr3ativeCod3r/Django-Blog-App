from django.views.generic import TemplateView


class AboutView(TemplateView):
    """About us page"""
    template_name = 'about/index.html'

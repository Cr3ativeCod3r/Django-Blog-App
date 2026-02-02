from django.views.generic import TemplateView


class MozgView(TemplateView):
    """Brain page"""
    template_name = 'mozg/index.html'

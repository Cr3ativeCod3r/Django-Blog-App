from django import template
from apps.banners.models import Banner

register = template.Library()


@register.simple_tag
def get_banners(position):
    """
    Get all active banners for a specific position.
    
    Usage in templates:
        {% load banner_tags %}
        {% get_banners 'header' as header_banners %}
    """
    return Banner.objects.filter(
        position=position,
        is_active=True
    ).order_by('order', '-created_at')

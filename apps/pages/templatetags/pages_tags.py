from django import template
from apps.posts.models import Category

register = template.Library()


@register.simple_tag
def get_categories():
    """
    Template tag to get all categories for navigation
    Usage: {% get_categories as categories %}
    """
    return Category.objects.all().order_by('name')

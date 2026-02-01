from django.contrib import admin
from django.utils.html import format_html
from .models import Banner


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['thumbnail_preview', 'position', 'link_preview', 'is_active', 'order', 'created_at']
    list_filter = ['position', 'is_active', 'created_at']
    list_editable = ['is_active', 'order']
    search_fields = ['link', 'position']
    ordering = ['position', 'order', '-created_at']
    
    fieldsets = (
        ('Banner Content', {
            'fields': ('image', 'link')
        }),
        ('Display Settings', {
            'fields': ('position', 'is_active', 'order')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at']
    
    def thumbnail_preview(self, obj):
        """Display thumbnail preview in admin list"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 60px; max-width: 120px;" />',
                obj.image.url
            )
        return '-'
    thumbnail_preview.short_description = 'Preview'
    
    def link_preview(self, obj):
        """Display truncated link with full URL as tooltip"""
        if len(obj.link) > 50:
            return format_html(
                '<span title="{}">{}</span>',
                obj.link,
                obj.link[:47] + '...'
            )
        return obj.link
    link_preview.short_description = 'Link'

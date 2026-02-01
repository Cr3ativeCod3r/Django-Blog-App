from django.contrib import admin
from .models import MedicalCenter


@admin.register(MedicalCenter)
class MedicalCenterAdmin(admin.ModelAdmin):
    list_display = ['department', 'address', 'lat', 'lng', 'created_at']
    search_fields = ['department', 'address', 'treatedDiseases']
    list_filter = ['created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Podstawowe informacje', {
            'fields': ('department', 'address', 'phone')
        }),
        ('Leczone choroby', {
            'fields': ('treatedDiseases',)
        }),
        ('Lokalizacja', {
            'fields': ('lat', 'lng')
        }),
        ('Metadane', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

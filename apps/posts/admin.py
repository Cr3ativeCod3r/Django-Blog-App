from django.contrib import admin
from .models import Category, Tag, Post, GalleryImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 1
    max_num = 12
    fields = ['image', 'caption', 'position']
    ordering = ['position']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'published', 'created_at']
    list_filter = ['published', 'category', 'created_at', 'tags']
    search_fields = ['title', 'excerpt', 'content']
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ['category', 'author', 'tags']
    
    fieldsets = (
        ('Basic information', {
            'fields': ('title', 'slug', 'category', 'author', 'published')
        }),
        ('Listing and Hero section', {
            'fields': ('hero_image', 'hero_youtube_url', 'excerpt'),
            'description': 'hero_image used for both tile and hero section. Priority: YouTube URL > Hero Image > Category Default Image'
        }),
        ('Content', {
            'fields': ('content',)
        }),
        ('Tags', {
            'fields': ('tags',),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [GalleryImageInline]
    
    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['post', 'caption', 'position', 'uploaded_at']
    list_filter = ['post__category', 'uploaded_at']
    search_fields = ['post__title', 'caption']
    autocomplete_fields = ['post']
    ordering = ['post', 'position']

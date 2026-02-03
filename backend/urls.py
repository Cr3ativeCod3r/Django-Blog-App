from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from apps.posts.sitemaps import PostSitemap, CategorySitemap
from apps.pages.sitemaps import StaticPagesSitemap

# Sitemaps configuration
sitemaps = {
    'posts': PostSitemap,
    'categories': CategorySitemap,
    'pages': StaticPagesSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', include('robots.urls')),
    path('', include('apps.pages.urls')),       # Strony statyczne
    path('', include('apps.posts.urls_web')),   # Widoki webowe postów
    path('', include('apps.map.urls')),         # Mapa ośrodków medycznych
    path('api/', include('apps.posts.urls')),   # API
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


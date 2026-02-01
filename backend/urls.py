from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.pages.urls')),       # Strony statyczne
    path('', include('apps.posts.urls_web')),   # Widoki webowe postów
    path('', include('apps.map.urls')),         # Mapa ośrodków medycznych
    path('api/', include('apps.posts.urls')),   # API
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


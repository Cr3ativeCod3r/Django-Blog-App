from django.urls import path
from .views import MapView, LocationsAPIView, ImportLocationsAPIView

urlpatterns = [
    # Map display page
    path('mapa/', MapView.as_view(), name='map'),
    
    # API endpoints
    path('api/map/locations/', LocationsAPIView.as_view(), name='api-locations'),
    path('api/map/import/', ImportLocationsAPIView.as_view(), name='api-import'),
]

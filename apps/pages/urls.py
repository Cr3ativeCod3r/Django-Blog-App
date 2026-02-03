from django.urls import path
from .home.views import HomeView
from .about.views import AboutView
from .contact.views import ContactView
from .search.views import SearchView
from apps.map.views import MapView
from .statut.views import StatutView
from .categories.views import CategoryListView, CategoryDetailView
from .foundation.views import FoundationView
from .mozg.views import MozgView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('o-nas/', AboutView.as_view(), name='about'),
    path('kontakt/', ContactView.as_view(), name='contact'),
    path('szukaj/', SearchView.as_view(), name='search'),
    path('mapa/', MapView.as_view(), name='mapa'),
    path('mozg/', MozgView.as_view(), name='mozg'),
    path('statut/', StatutView.as_view(), name='statut'),
    path('fundacja/', FoundationView.as_view(), name='foundation'),
    
    # Category pages
    path('kategorie/', CategoryListView.as_view(), name='category_list'),
    path('kategorie/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),
]

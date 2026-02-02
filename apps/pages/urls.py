from django.urls import path
from .home.views import HomeView
from .about.views import AboutView
from .contact.views import ContactView
from .search.views import SearchView
from .mozg.views import MozgView
from .statut.views import StatutView
from .categories.views import CategoryListView, CategoryDetailView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('o-nas/', AboutView.as_view(), name='about'),
    path('kontakt/', ContactView.as_view(), name='contact'),
    path('szukaj/', SearchView.as_view(), name='search'),
    path('mozg/', MozgView.as_view(), name='mozg'),
    path('statut/', StatutView.as_view(), name='statut'),
    
    # Category pages
    path('kategorie/', CategoryListView.as_view(), name='category_list'),
    path('kategorie/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),
]

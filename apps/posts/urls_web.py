from django.urls import path
from .views import PostDetailView

urlpatterns = [
    path('<slug:category_slug>/<slug:post_slug>/', PostDetailView.as_view(), name='post_detail'),
]

from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from .models import Category, Tag, Post
from .serializers import (
    CategorySerializer, TagSerializer, PostListSerializer,
    PostDetailSerializer, PostCreateUpdateSerializer
)


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Allows read access to all, but modifications only to admin
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for categories
    GET - publicly available
    POST/PUT/PATCH/DELETE - admin only
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]
    lookup_field = 'slug'
    
    @action(detail=True, methods=['get'])
    def posts(self, request, slug=None):
        """Returns posts from given category"""
        category = self.get_object()
        posts = Post.objects.published().by_category(category.slug).with_relations()
        serializer = PostListSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)


class TagViewSet(viewsets.ModelViewSet):
    """
    ViewSet for tags
    GET - publicly available
    POST/PUT/PATCH/DELETE - admin only
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    lookup_field = 'slug'
    
    @action(detail=True, methods=['get'])
    def posts(self, request, slug=None):
        """Returns posts with given tag"""
        tag = self.get_object()
        posts = Post.objects.published().by_tag(tag.slug).with_relations()
        serializer = PostListSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for posts
    GET - publicly available (only published for non-admin)
    POST/PUT/PATCH/DELETE - admin only
    """
    queryset = Post.objects.all()
    permission_classes = [IsAdminUserOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__slug', 'tags__slug', 'published', 'author']
    search_fields = ['title', 'excerpt', 'content']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        Admin sees all posts
        Anonymous/regular users see only published posts
        """
        queryset = Post.objects.with_relations()
        
        if not self.request.user.is_staff:
            queryset = queryset.published()
        
        return queryset
    
    def get_serializer_class(self):
        """
        Returns appropriate serializer depending on action
        """
        if self.action == 'list':
            return PostListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return PostCreateUpdateSerializer
        return PostDetailSerializer
    
    
    @action(detail=False, methods=['get'])
    def published(self, request):
        """Returns only published posts"""
        posts = self.get_queryset().published()
        page = self.paginate_queryset(posts)
        
        if page is not None:
            serializer = PostListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = PostListSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)


class PostDetailView(DetailView):
    """
    Post detail view
    URL: /<category_slug>/<post_slug>/
    """
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'
    
    def get_object(self):
        return get_object_or_404(
            Post.objects.published().with_relations().prefetch_related('gallery_images'),
            category__slug=self.kwargs['category_slug'],
            slug=self.kwargs['post_slug']
        )

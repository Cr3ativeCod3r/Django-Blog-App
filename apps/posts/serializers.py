from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Tag, Post, GalleryImage


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for categories"""
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'default_image']
        read_only_fields = ['slug']


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags"""
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']
        read_only_fields = ['slug']


class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for author (User)"""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class GalleryImageSerializer(serializers.ModelSerializer):
    """Serializer for gallery images"""
    class Meta:
        model = GalleryImage
        fields = ['id', 'image', 'caption', 'position', 'uploaded_at']
        read_only_fields = ['uploaded_at']


class PostListSerializer(serializers.ModelSerializer):
    """Serializer for post listing (simplified version)"""
    category = CategorySerializer(read_only=True)
    author = AuthorSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    url = serializers.SerializerMethodField()
    thumbnail_image = serializers.ImageField(source='hero_image', read_only=True)
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'created_at', 'published',
            'thumbnail_image', 'excerpt', 'category', 'author', 'tags', 'url'
        ]
    
    def get_url(self, obj):
        return obj.get_url()


class PostDetailSerializer(serializers.ModelSerializer):
    """Serializer for full post data (with content and relations)"""
    category = CategorySerializer(read_only=True)
    author = AuthorSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    related_posts = serializers.SerializerMethodField()
    gallery_images = GalleryImageSerializer(many=True, read_only=True)
    hero_media = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    thumbnail_image = serializers.ImageField(source='hero_image', read_only=True)
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'created_at', 'published',
            'thumbnail_image', 'excerpt',
            'hero_image', 'hero_youtube_url', 'hero_media',
            'content', 'category', 'author', 'tags',
            'related_posts', 'gallery_images', 'url'
        ]
    
    def get_related_posts(self, obj):
        """Returns up to 6 random posts from database (excluding current post)"""
        from django.db.models import Q
        
        # Get max 6 random published posts, excluding current one
        random_posts = Post.objects.filter(
            published=True
        ).exclude(
            id=obj.id
        ).order_by('?')[:6]
        
        # Use simplified serializer for related posts
        return PostListSerializer(random_posts, many=True, context=self.context).data
    
    def get_hero_media(self, obj):
        return obj.get_hero_media()
    
    def get_url(self, obj):
        return obj.get_url()


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/editing posts"""
    tags = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Tag.objects.all(), 
        required=False
    )
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'published',
            'excerpt', 'hero_image', 'hero_youtube_url',
            'content', 'category', 'author', 'tags'
        ]
        read_only_fields = ['id']
    
    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        post = Post.objects.create(**validated_data)
        post.tags.set(tags)
        return post
    
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if tags is not None:
            instance.tags.set(tags)
        
        return instance

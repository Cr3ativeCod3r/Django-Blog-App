from django.db import models
from django.db.models import Q


class CategoryQuerySet(models.QuerySet):
    """QuerySet for Category model"""
    
    def with_post_count(self):
        """Annotate categories with number of published posts"""
        return self.annotate(
            post_count=models.Count('posts', filter=Q(posts__published=True))
        )


class CategoryManager(models.Manager):
    """Manager for Category model"""
    
    def get_queryset(self):
        return CategoryQuerySet(self.model, using=self._db)
    
    def with_post_count(self):
        return self.get_queryset().with_post_count()


class TagQuerySet(models.QuerySet):
    """QuerySet for Tag model"""
    
    def with_post_count(self):
        """Annotate tags with number of published posts"""
        return self.annotate(
            post_count=models.Count('posts', filter=Q(posts__published=True))
        )
    
    def popular(self, limit=10):
        """Return most popular tags by post count"""
        return self.with_post_count().order_by('-post_count')[:limit]


class TagManager(models.Manager):
    """Manager for Tag model"""
    
    def get_queryset(self):
        return TagQuerySet(self.model, using=self._db)
    
    def with_post_count(self):
        return self.get_queryset().with_post_count()
    
    def popular(self, limit=10):
        return self.get_queryset().popular(limit)


class PostQuerySet(models.QuerySet):
    """QuerySet for Post model"""
    
    def published(self):
        """Return only published posts"""
        return self.filter(published=True)
    
    def with_relations(self):
        """Optimize query with select_related and prefetch_related"""
        return self.select_related('category', 'author').prefetch_related('tags')
    
    def by_category(self, category_slug):
        """Filter posts by category slug"""
        return self.filter(category__slug=category_slug)
    
    def by_tag(self, tag_slug):
        """Filter posts by tag slug"""
        return self.filter(tags__slug=tag_slug)
    
    def search(self, query):
        """Search posts by title or content"""
        return self.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
    
    def search_title_first(self, query):
        """Search by title first, then by content if no results"""
        title_results = self.filter(title__icontains=query)
        if title_results.exists():
            return title_results
        return self.filter(content__icontains=query)
    
    def by_tags_list(self, tag_slugs):
        """Filter posts that have any of the specified tags"""
        return self.filter(tags__slug__in=tag_slugs).distinct()
    
    def featured(self, limit=6):
        """Return featured posts (most recent published)"""
        return self.published().order_by('-created_at')[:limit]


class PostManager(models.Manager):
    """Manager for Post model"""
    
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)
    
    def published(self):
        return self.get_queryset().published()
    
    def with_relations(self):
        return self.get_queryset().with_relations()
    
    def by_category(self, category_slug):
        return self.get_queryset().by_category(category_slug)
    
    def by_tag(self, tag_slug):
        return self.get_queryset().by_tag(tag_slug)
    
    def search(self, query):
        return self.get_queryset().search(query)
    
    def search_title_first(self, query):
        return self.get_queryset().search_title_first(query)
    
    def by_tags_list(self, tag_slugs):
        return self.get_queryset().by_tags_list(tag_slugs)
    
    def featured(self, limit=6):
        return self.get_queryset().featured(limit)


class GalleryImageQuerySet(models.QuerySet):
    """QuerySet for GalleryImage model"""
    
    def for_post(self, post):
        """Return gallery images for a specific post"""
        return self.filter(post=post).order_by('position', 'uploaded_at')
    
    def ordered(self):
        """Return gallery images ordered by position"""
        return self.order_by('position', 'uploaded_at')


class GalleryImageManager(models.Manager):
    """Manager for GalleryImage model"""
    
    def get_queryset(self):
        return GalleryImageQuerySet(self.model, using=self._db)
    
    def for_post(self, post):
        return self.get_queryset().for_post(post)
    
    def ordered(self):
        return self.get_queryset().ordered()

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from ckeditor.fields import RichTextField


class Category(models.Model):
    """Thematic category for the portal"""
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    default_image = models.ImageField(upload_to='categories/', null=True, blank=True)
    
    class Meta:
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategorie"
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Tag(models.Model):
    """Thematic tag"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, db_index=True)
    
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tagi"
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Post(models.Model):
    """Main content entity - Post"""
    # Basic fields
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    published = models.BooleanField(default=False)
    
    # Data for listing and hero section (one image serves both purposes)
    hero_image = models.ImageField(upload_to='posts/heroes/', null=True, blank=True)
    excerpt = models.TextField(max_length=500, help_text="Preview description for listing display")
    
    # Hero YouTube (optional, instead of image)
    hero_youtube_url = models.URLField(max_length=500, null=True, blank=True)
    
    # Content
    content = RichTextField()
    
    # Relations
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    
    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posty"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['published', '-created_at']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_hero_media(self):
        """
        Business rule: hero media priority
        1. hero_youtube_url → video
        2. hero_image → image
        3. category.default_image → fallback
        """
        if self.hero_youtube_url:
            return {'type': 'youtube', 'url': self.hero_youtube_url}
        elif self.hero_image:
            return {'type': 'image', 'url': self.hero_image.url}
        elif self.category and self.category.default_image:
            return {'type': 'image', 'url': self.category.default_image.url}
        return None
    
    def get_url(self):
        """Post URL: /{category.slug}/{post.slug}"""
        return f"/{self.category.slug}/{self.slug}"
    
    def __str__(self):
        return self.title


def gallery_image_upload_path(instance, filename):
    """Defines gallery image save path: media/gallery/{post-slug}/{filename}"""
    import os
    from django.utils.text import slugify
    
    # Get file extension
    ext = os.path.splitext(filename)[1]
    # Create filename with timestamp
    from datetime import datetime
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    new_filename = f"{timestamp}{ext}"
    
    return f"gallery/{instance.post.slug}/{new_filename}"


class GalleryImage(models.Model):
    """Image in post gallery"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to=gallery_image_upload_path)
    caption = models.CharField(max_length=200, blank=True, help_text="Optional image caption")
    position = models.PositiveIntegerField(default=0, help_text="Display order")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Zdjęcie galerii"
        verbose_name_plural = "Zdjęcia galerii"
        ordering = ['position', 'uploaded_at']
        indexes = [
            models.Index(fields=['post', 'position']),
        ]
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.post:
            existing_count = GalleryImage.objects.filter(post=self.post).exclude(pk=self.pk).count()
            if existing_count >= 12:
                raise ValidationError("Post can have a maximum of 12 images in gallery")
    
    def __str__(self):
        return f"Gallery image: {self.post.title} ({self.position})"

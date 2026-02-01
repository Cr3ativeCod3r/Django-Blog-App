from django.db import models


class Banner(models.Model):
    """Promotional banner for display on the website"""
    
    POSITION_CHOICES = [
        ('home_banner_1', 'Home Banner 1 (after 3 posts)'),
        ('home_banner_2', 'Home Banner 2 (after 6 posts)'),
        ('home_banner_3', 'Home Banner 3 (after 12 posts)'),
    ]
    
    image = models.ImageField(
        upload_to='banners/',
        help_text="Banner image (recommended height: ~300px, full width)"
    )
    link = models.URLField(
        max_length=500,
        help_text="Destination URL when banner is clicked"
    )
    position = models.CharField(
        max_length=50,
        choices=POSITION_CHOICES,
        db_index=True,
        help_text="Display location on the website"
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Whether this banner is currently active"
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order (lower numbers appear first)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Banery"
        ordering = ['position', 'order', '-created_at']
        indexes = [
            models.Index(fields=['position', 'is_active', 'order']),
        ]
    
    def __str__(self):
        return f"Banner ({self.get_position_display()}) - {self.link[:50]}"

from django.db import models


class BannerQuerySet(models.QuerySet):
    """QuerySet for Banner model"""
    
    def active(self):
        """Return only active banners"""
        return self.filter(is_active=True)
    
    def for_position(self, position):
        """Filter banners by position"""
        return self.filter(position=position).order_by('order', '-created_at')
    
    def active_for_position(self, position):
        """Return active banners for specific position"""
        return self.active().for_position(position)


class BannerManager(models.Manager):
    """Manager for Banner model"""
    
    def get_queryset(self):
        return BannerQuerySet(self.model, using=self._db)
    
    def active(self):
        return self.get_queryset().active()
    
    def for_position(self, position):
        return self.get_queryset().for_position(position)
    
    def active_for_position(self, position):
        return self.get_queryset().active_for_position(position)

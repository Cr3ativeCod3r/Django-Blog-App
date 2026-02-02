from django.db import models
from django.db.models import Q


class MedicalCenterQuerySet(models.QuerySet):
    """QuerySet for MedicalCenter model"""
    
    def by_disease(self, disease):
        """Filter medical centers that treat a specific disease"""
        return self.filter(treatedDiseases__icontains=disease)
    
    def search(self, query):
        """Search medical centers by department name, address, or diseases"""
        return self.filter(
            Q(department__icontains=query) |
            Q(address__icontains=query) |
            Q(treatedDiseases__icontains=query)
        )
    
    def near_location(self, lat, lng, lat_range=0.5, lng_range=0.5):
        """
        Find medical centers near a location
        Uses simple bounding box (not precise distance calculation)
        """
        return self.filter(
            lat__gte=lat - lat_range,
            lat__lte=lat + lat_range,
            lng__gte=lng - lng_range,
            lng__lte=lng + lng_range
        )


class MedicalCenterManager(models.Manager):
    """Manager for MedicalCenter model"""
    
    def get_queryset(self):
        return MedicalCenterQuerySet(self.model, using=self._db)
    
    def by_disease(self, disease):
        return self.get_queryset().by_disease(disease)
    
    def search(self, query):
        return self.get_queryset().search(query)
    
    def near_location(self, lat, lng, lat_range=0.5, lng_range=0.5):
        return self.get_queryset().near_location(lat, lng, lat_range, lng_range)

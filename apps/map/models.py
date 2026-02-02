from django.db import models
from .managers import MedicalCenterManager


class MedicalCenter(models.Model):
    """Medical center/department location"""
    department = models.CharField(
        max_length=500,
        verbose_name="Nazwa oddziału/ośrodka",
        help_text="Pełna nazwa oddziału lub ośrodka medycznego"
    )
    treatedDiseases = models.TextField(
        verbose_name="Leczone choroby",
        help_text="Lista chorób oddzielona przecinkami"
    )
    address = models.TextField(
        verbose_name="Adres",
        help_text="Pełny adres ośrodka"
    )
    phone = models.TextField(
        verbose_name="Telefon",
        help_text="Numery telefonów kontaktowych"
    )
    lat = models.FloatField(
        verbose_name="Szerokość geograficzna",
        help_text="Latitude"
    )
    lng = models.FloatField(
        verbose_name="Długość geograficzna",
        help_text="Longitude"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = MedicalCenterManager()
    
    class Meta:
        verbose_name = "Ośrodek Medyczny"
        verbose_name_plural = "Ośrodki Medyczne"
        ordering = ['department']
        indexes = [
            models.Index(fields=['lat', 'lng']),
            models.Index(fields=['department']),
        ]
    
    def __str__(self):
        return self.department
    
    def get_diseases_list(self):
        """Return list of treated diseases"""
        return [disease.strip() for disease in self.treatedDiseases.split(',')]

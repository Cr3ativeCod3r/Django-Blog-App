from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
import requests

from .models import MedicalCenter
from .serializers import MedicalCenterSerializer

class MapView(TemplateView):
    """Main map view displaying all medical centers"""
    template_name = 'map/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # SEO Context
        meta_title = 'Mapa placówek medycznych - Fundacja Chorób Mózgu'
        meta_description = 'Mapa placówek medycznych zajmujących się leczeniem chorób mózgu. Znajdź specjalistów i centra medyczne w całej Polsce.'
        
        context.update({
            # Basic Meta
            'meta_title': meta_title,
            'meta_description': meta_description,
            'meta_keywords': 'mapa placówek medycznych, choroby mózgu, neurologia, leczenie, szpitale',
            'canonical_url': self.request.build_absolute_uri(),  # DODAJ TO
            
            # Open Graph
            'og_type': 'website',
            'og_title': meta_title,
            'og_description': meta_description,
            'og_url': self.request.build_absolute_uri(),
            'og_image': '/static/images/og-default.jpg',
            
            # Twitter Card
            'twitter_title': meta_title,
            'twitter_description': meta_description,
        })
        
        return context

class LocationsAPIView(generics.ListAPIView):
    """API endpoint returning all medical centers with optional filtering"""
    serializer_class = MedicalCenterSerializer
    pagination_class = None  # Disable pagination to return all results
    
    def get_queryset(self):
        queryset = MedicalCenter.objects.all()
        
        # Filter by disease if provided
        disease = self.request.query_params.get('disease', None)
        if disease:
            queryset = queryset.filter(treatedDiseases__icontains=disease)
        
        # Filter by search term (department name)
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(department__icontains=search)
        
        return queryset


class ImportLocationsAPIView(APIView):
    """Protected endpoint for importing data from external API"""
    
    def post(self, request):
        # Check API key
        api_key = request.headers.get('X-API-Key')
        expected_key = getattr(settings, 'MAP_API_KEY', None)
        
        if not expected_key:
            return Response(
                {'error': 'MAP_API_KEY not configured on server'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        if api_key != expected_key:
            return Response(
                {'error': 'Invalid or missing API key'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Fetch data from external API
        try:
            response = requests.get('https://chorobymozgu.pl/api/map/locations', timeout=30)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            return Response(
                {'error': f'Failed to fetch data from external API: {str(e)}'},
                status=status.HTTP_502_BAD_GATEWAY
            )
        except ValueError as e:
            return Response(
                {'error': f'Invalid JSON response from external API: {str(e)}'},
                status=status.HTTP_502_BAD_GATEWAY
            )
        
        # Import data
        imported = 0
        updated = 0
        errors = []
        
        for item in data:
            try:
                # Use _id from external API as unique identifier if available
                external_id = item.get('_id')
                
                # Check if center already exists by matching department and address
                existing = MedicalCenter.objects.filter(
                    department=item['department'],
                    address=item['address']
                ).first()
                
                if existing:
                    # Update existing record
                    existing.treatedDiseases = item['treatedDiseases']
                    existing.phone = item['phone']
                    existing.lat = item['lat']
                    existing.lng = item['lng']
                    existing.save()
                    updated += 1
                else:
                    # Create new record
                    MedicalCenter.objects.create(
                        department=item['department'],
                        treatedDiseases=item['treatedDiseases'],
                        address=item['address'],
                        phone=item['phone'],
                        lat=item['lat'],
                        lng=item['lng']
                    )
                    imported += 1
                    
            except KeyError as e:
                errors.append(f"Missing field in item: {str(e)}")
            except Exception as e:
                errors.append(f"Error importing item: {str(e)}")
        
        return Response({
            'success': True,
            'imported': imported,
            'updated': updated,
            'total_processed': imported + updated,
            'errors': errors if errors else None
        }, status=status.HTTP_200_OK)

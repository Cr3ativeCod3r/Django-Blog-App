from django.core.management.base import BaseCommand
import requests
from apps.map.models import MedicalCenter


class Command(BaseCommand):
    help = 'Import medical centers data from external API'

    def handle(self, *args, **options):
        self.stdout.write('Fetching data from https://chorobymozgu.pl/api/map/locations...')
        
        try:
            response = requests.get('https://chorobymozgu.pl/api/map/locations', timeout=30)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f'Failed to fetch data: {str(e)}'))
            return
        except ValueError as e:
            self.stdout.write(self.style.ERROR(f'Invalid JSON response: {str(e)}'))
            return
        
        self.stdout.write(f'Found {len(data)} locations. Importing...')
        
        imported = 0
        updated = 0
        errors = []
        
        for item in data:
            try:
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
                    self.stdout.write(f'  Updated: {existing.department[:50]}...')
                else:
                    # Create new record
                    center = MedicalCenter.objects.create(
                        department=item['department'],
                        treatedDiseases=item['treatedDiseases'],
                        address=item['address'],
                        phone=item['phone'],
                        lat=item['lat'],
                        lng=item['lng']
                    )
                    imported += 1
                    self.stdout.write(f'  Imported: {center.department[:50]}...')
                    
            except KeyError as e:
                error_msg = f"Missing field in item: {str(e)}"
                errors.append(error_msg)
                self.stdout.write(self.style.WARNING(f'  {error_msg}'))
            except Exception as e:
                error_msg = f"Error importing item: {str(e)}"
                errors.append(error_msg)
                self.stdout.write(self.style.WARNING(f'  {error_msg}'))
        
        self.stdout.write(self.style.SUCCESS(f'\n✓ Import completed!'))
        self.stdout.write(self.style.SUCCESS(f'  New centers imported: {imported}'))
        self.stdout.write(self.style.SUCCESS(f'  Existing centers updated: {updated}'))
        self.stdout.write(self.style.SUCCESS(f'  Total processed: {imported + updated}'))
        
        if errors:
            self.stdout.write(self.style.WARNING(f'  Errors encountered: {len(errors)}'))

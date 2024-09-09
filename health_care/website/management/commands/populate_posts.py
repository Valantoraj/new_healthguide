'''from website.models import Login
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Populate the database with some initial data'

    def handle(self, *args, **kwargs):
        # Create some initial data
        Login.objects.create(username='user2', password='password2')'''

# myapp/management/commands/import_medicine.py
import csv
from django.core.management.base import BaseCommand
from website.models import Medicine

class Command(BaseCommand):
    help = 'Import data from a CSV file into the Medicine model'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        try:
            with open(csv_file, newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Extract fields from the CSV row
                    sub_category = row.get('sub_category', '')
                    product_name = row.get('product_name', '')
                    salt_composition = row.get('salt_composition', '')
                    product_price = row.get('product_price', '')
                    product_manufactured = row.get('product_manufactured', '')
                    medicine_desc = row.get('medicine_desc', '')
                    side_effects = row.get('side_effects', '')
                    drug_interactions = row.get('drug_interactions', '')
                    
                    # Create or update the Medicine instance
                    medicine, created = Medicine.objects.update_or_create(
                        product_name=product_name,
                        defaults={
                            'sub_category': sub_category,
                            'salt_composition': salt_composition,
                            'product_price': product_price,
                            'product_manufactured': product_manufactured,
                            'medicine_desc': medicine_desc,
                            'side_effects': side_effects,
                            'drug_interactions': drug_interactions
                        },
                    )
                    
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Successfully created medicine: {product_name}'))
                    else:
                        self.stdout.write(self.style.SUCCESS(f'Successfully updated medicine: {product_name}'))
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f'File not found: {csv_file}'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'An error occurred: {e}'))


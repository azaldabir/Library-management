import requests
import json
from django.core.management.base import BaseCommand
from app.models import Book  

class Command(BaseCommand):
    help = 'Import books data from API'

    def handle(self, *args, **options):
        url = "https://frappe.io/api/method/frappe-library?page=2&title=and"
        response = requests.get(url)

        if response.status_code == 200:
            data = json.loads(response.text)  
            print(f"{data}")
            for item in data.get('message', []):  
                Book.objects.create(
                    bookID=item.get('bookID'),
                    title=item.get('title'),
                    authors=item.get('authors'),
                    average_rating=float(item.get('average_rating')),
                    isbn=item.get('isbn'),
                    isbn13=item.get('isbn13'),
                    language_code=item.get('language_code'),
                    num_pages=int(item.get("  num_pages")),
                    ratings_count=int(item.get('ratings_count')),
                    text_reviews_count=int(item.get('text_reviews_count')),
                    publication_date=item.get('publication_date'),
                    publisher=item.get('publisher'),
                    stock_quantity=0  
                )
            self.stdout.write(self.style.SUCCESS('Successfully imported books'))
        else:
            self.stdout.write(self.style.ERROR('Failed to fetch data from the API'))

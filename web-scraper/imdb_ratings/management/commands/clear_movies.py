from django.core.management.base import BaseCommand
from imdb_ratings.models import Movie

class Command(BaseCommand):
    help = 'Clears all movies from the database'

    def handle(self, *args, **kwargs):
        Movie.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully cleared all movies from the database.'))
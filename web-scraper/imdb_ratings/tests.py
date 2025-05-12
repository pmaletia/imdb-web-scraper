from django.test import TestCase
from imdb_ratings.models import Movie

class MovieModelTest(TestCase):
    def test_create_movie(self):
        movie = Movie.objects.create(
            title="Test Movie",
            release_year="2023",
            imdb_rating=7.5,
            directors="Director A",
            cast="Actor X, Actor Y",
            plot_summary="Test summary"
        )
        self.assertEqual(movie.title, "Test Movie")

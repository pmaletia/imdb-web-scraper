from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255, unique=True, db_index=True)
    release_year = models.CharField(max_length=20, blank=True)
    imdb_rating = models.FloatField(null=True, blank=True)
    directors = models.TextField(blank=True)
    cast = models.TextField(blank=True)
    plot_summary = models.TextField(blank=True)
    genre = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title

# Generated by Django 5.2.1 on 2025-05-12 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("imdb_ratings", "0002_movie_movie_url_alter_movie_title"),
    ]

    operations = [
        migrations.RemoveField(model_name="movie", name="movie_url",),
        migrations.AddField(
            model_name="movie",
            name="genre",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]

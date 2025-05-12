from django.urls import path, include
from .views import MovieSearchView, ScrapeView
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet

router = DefaultRouter()
router.register(r'api/imdb_ratings', MovieViewSet)

urlpatterns = [
    path('movie-search/', MovieSearchView.as_view(), name='movie-search'),  # For searching movies
    path('scrape/', ScrapeView.as_view(), name='scrape-movies'),  # For scraping movies
    path('', include(router.urls)),
]
# Create your views here.
from rest_framework import viewsets
from .models import Movie
from .serializer import MovieSerializer
from django.views.generic import ListView
from django.db.models import Q
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.generic.edit import FormView
from django import forms
from .scraper import scrape_movies

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class MovieSearchView(ListView):
    model = Movie
    template_name = 'imdb_ratings/movie_list.html'  # Updated template path
    context_object_name = 'imdb_ratings_movie'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        base_queryset = super().get_queryset()
        if query:
            return base_queryset.filter(
                Q(title__icontains=query) |
                Q(directors__icontains=query) |
                Q(genre__icontains=query)
            ).order_by('-imdb_rating')
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("this is the context data")   
        print(f"Pagination Context: {context['imdb_ratings_movie']}") 
        context['query'] = self.request.GET.get('q', '')
        return context

class ScrapeForm(forms.Form):
    genre = forms.CharField(label='Genre or Keyword', max_length=100)
    no_of_pages = forms.IntegerField(label='Number of Pages', initial=5, min_value=1)

@method_decorator(csrf_exempt, name='dispatch')
class ScrapeView(FormView):
    form_class = ScrapeForm
    template_name = 'imdb_ratings/scrape_form.html'  # Separate template for scraping

    def form_valid(self, form):
        genre = form.cleaned_data['genre']
        max_pages = form.cleaned_data['no_of_pages']
        scrape_movies(genre, max_pages=max_pages, concurrency=5)
        messages.success(self.request, f"Scraped movies for genre: {genre}")
        # Redirect to the correct movie search page with the scraped genre
        redirect_url = f"/api/movie-search/?q={genre}"  # Use absolute path
        return redirect(redirect_url)

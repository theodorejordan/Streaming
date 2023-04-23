from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from streaming.models import Movie, SubscriptionPlan, UserProfile, Review

# Create your views here.
def index(request):
    movies = Movie.objects.annotate(num_reviews = Count('reviews')).all()
    movies = sorted(movies, key = lambda movie: movie.average_rating(), reverse = True)
    return render(request, 'streaming/index.html', {'movies': movies})

def movie(request, movie_id):
    try:
        print(Movie.objects.get(pk=movie_id))
        movie = Movie.objects.get(pk=movie_id)
        return render(request, 'streaming/movie.html', {'movie': movie})
    except ObjectDoesNotExist:
        raise Http404('Movie not found')

def user_reviews(request, user_id):
    try:
        user = UserProfile.objects.get(pk = user_id)
        reviews = Review.objects.filter(user = user)
        return render(request, 'streaming/user_reviews.html', {'reviews': reviews})
    except ObjectDoesNotExist:
        raise Http404('User not found')
    
def subscription_plan(request, subscription_id):
    subscription_plan = get_object_or_404(SubscriptionPlan, pk = subscription_id)
    movies = subscription_plan.movies.all()
    return render(request, 'streaming/subscription_plan.html', {'movies': movies})
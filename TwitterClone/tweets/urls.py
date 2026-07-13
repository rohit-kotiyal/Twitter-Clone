from .views import create_tweet
from django.urls import path


urlpatterns = [
    path('create-tweet/', create_tweet, name='create_tweet'),
]





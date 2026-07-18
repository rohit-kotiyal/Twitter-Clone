from .views import create_tweet, feed, delete_tweet, edit_tweet, toggle_like, comment_section
from django.urls import path


urlpatterns = [
    path('create-tweet/', create_tweet, name='create_tweet'),
    path('feed/', feed, name='feed'),
    path('delete-tweet/<int:tweet_id>/', delete_tweet, name='delete_tweet'),
    path('edit/<int:tweet_id>/', edit_tweet, name='edit_tweet'),
    path('toggle-like/<int:tweet_id>/', toggle_like, name='toggle_like'),
    path('<int:tweet_id>/', comment_section, name='comment_section'),
]





from django.urls import path
from .views import toggle_follow

urlpatterns = [
    path('toggle-follow/<int:user_id>/', toggle_follow, name='toggle_follow'),
]

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from .models import Follow
from django.contrib.auth.decorators import login_required



# Create your views here.
@login_required
def toggle_follow(request, user_id):
    target_user = get_object_or_404(User, pk=user_id)

    if request.user == target_user:
        return HttpResponseForbidden("You can't follow yourself.")

    follow = Follow.objects.filter(follower=request.user, followed=target_user)

    if(follow.exists()):
        follow.delete()

    else:    
        follow.create(follower=request.user, followed=target_user)

    return redirect('feed')
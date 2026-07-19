from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden, JsonResponse
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
    is_follow = None

    if(follow.exists()):
        is_follow = False
        follow.delete()

    else:
        is_follow = True    
        follow.create(follower=request.user, followed=target_user)

    return JsonResponse({"is_follow": is_follow, "follower_count": target_user.followers.count()})
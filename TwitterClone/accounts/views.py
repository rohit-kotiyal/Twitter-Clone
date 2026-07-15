from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm
from django.contrib.auth.models import User
from tweets.models import Tweet
from follows.models import Follow


# Create your views here.

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        
    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})



def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    tweets = Tweet.objects.filter(author=profile_user).order_by('-created_at')
    followers = profile_user.followers.count()
    followings = profile_user.following.count()

    is_following = Follow.objects.filter(follower=request.user, followed=profile_user).exists()

    context_dict = {
        'profile_user': profile_user,
        'tweets': tweets,
        'followers': followers,
        'following': followings,
        'is_following': is_following
    }

    return render(request, 'accounts/profile.html', context_dict)

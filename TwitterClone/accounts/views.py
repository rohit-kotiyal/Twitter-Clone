from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm
from django.contrib.auth.models import User
from tweets.models import Tweet
from follows.models import Follow
from django.core.paginator import Paginator


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
    paginator = Paginator(tweets, 1)
    page_number = request.GET.get('page', 5)
    page_obj = paginator.get_page(page_number)
    followers = profile_user.followers.count()
    followings = profile_user.following.count()

    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user, followed=profile_user).exists()
    else:
        is_following = False

    context_dict = {
        'profile_user': profile_user,
        'page_obj': page_obj,
        'followers': followers,
        'following': followings,
        'is_following': is_following
    }

    return render(request, 'accounts/profile.html', context_dict)

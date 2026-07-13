from django.shortcuts import render, redirect
from .forms import TweetForm
from django.contrib.auth.decorators import login_required
from .models import Tweet


# Create your views here.

@login_required
def create_tweet(request):
    if request.method == "POST":
        form = TweetForm(request.POST)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.author = request.user
            tweet.save()
            return redirect('feed')
        
    else:
        form = TweetForm()

    return render(request, 'tweets/create_tweet.html', {'form': form})



def feed(request):
    tweets = Tweet.objects.all().order_by('-created_at')

    return render(request, 'tweets/feed.html', {'tweets': tweets})
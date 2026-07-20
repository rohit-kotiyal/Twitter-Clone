from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponseNotAllowed, JsonResponse
from .forms import TweetForm, CommentForm
from django.contrib.auth.decorators import login_required
from .models import Tweet, Like, Comment


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



@login_required
def delete_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    if tweet.author != request.user:
        return HttpResponseForbidden("You can't delete this tweet.")
    
    if request.method == 'POST':
        tweet.delete()
        return redirect('feed')

    return HttpResponseNotAllowed(['POST'])


@login_required
def edit_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)

    if(tweet.author != request.user):
        return HttpResponseForbidden("You can't edit this tweet.")
    
    if request.method == 'POST':
        form = TweetForm(request.POST, instance=tweet)

        if form.is_valid():
            form.save()
            return redirect('feed')
    else:
        form = TweetForm(instance=tweet)

    return render(request, 'tweets/edit_tweet.html', {'form': form})




@login_required
def toggle_like(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)

    like = Like.objects.filter(user=request.user, tweet=tweet)
    is_liked_now = None

    if(like.exists()):
        is_liked_now = False
        like.delete()

    else:
        is_liked_now = True
        like.create(user=request.user, tweet=tweet)

    return JsonResponse({'liked': is_liked_now, 'like_count': like.count()})



def feed(request):
    tweets = Tweet.objects.all().order_by('-created_at')

    if request.user.is_authenticated:
        liked_tweet_ids = set(Like.objects.filter(user=request.user).values_list('tweet_id', flat=True))
    else:
        liked_tweet_ids = set()
    
    return render(request, 'tweets/feed.html', {'tweets': tweets, 'liked_tweet_ids': liked_tweet_ids})



def comment_section(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    comments = tweet.comments.filter(parent=None).order_by('-created_at')

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.tweet = tweet
            comment.author = request.user
            parent_id = request.POST.get('parent_id')
            
            if parent_id:
                comment.parent = get_object_or_404(Comment, pk=parent_id)
            
            comment.save()
            return redirect('comment_section', tweet_id=tweet.id)
        
    else:
        form = CommentForm()

    return render(request, 'tweets/comments.html', {'comments': comments, 'tweet': tweet, 'form': form})



@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author != request.user:
        return HttpResponseForbidden("You can't delete this comment.")
    
    else:
        if request.method == "POST":
            tweet_id = comment.tweet.id
            comment.delete()
            return redirect('comment_section', tweet_id=tweet_id)

    return HttpResponseNotAllowed(['POST'])





def search(request):
    query = request.GET.get('q', '')
    
    if not query:
        return redirect('feed')
    
    tweets = Tweet.objects.filter(content__icontains=query)


    return render(request, 'tweets/search.html', {'tweets': tweets, 'query': query})


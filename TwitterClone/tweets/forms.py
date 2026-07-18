from django import forms
from .models import Tweet, Comment

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
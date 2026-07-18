from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Tweet(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tweets')
    content = models.CharField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.author.username} - {self.content[:10]}"
    


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} liked {self.tweet} tweet."
    

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'tweet'], name='unique_like')
        ]
    
    


class Comment(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    content = models.CharField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.author} commented {self.content[:10]}"
    
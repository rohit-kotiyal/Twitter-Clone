from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Tweet(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tweets')
    content = models.CharField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.author.username} - {self.content[:10]}"
    



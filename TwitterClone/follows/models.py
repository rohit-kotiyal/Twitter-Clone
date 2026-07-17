from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"
    

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower', 'followed'], name='unique_follow'),
            models.CheckConstraint(condition=~models.Q(follower=models.F('followed')), name='no_self_follow')
        ]
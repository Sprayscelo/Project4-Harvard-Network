from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    following = models.ManyToManyField("User", related_name="followers")
    pass
    def __str__(self):
        return f"{self.username}"
    
    def serialize(self): 
        FollowersPosts = [teste.username for teste in self.following.all()]
        return {
            "userID": self.id,
            "username": self.username,
            "followers": len(self.followers.all()),
            "following": len(self.following.all()),
            "posts": [{"content": teste["content"], "timestamp": teste["timestamp"].strftime("%b %d %Y, %I:%M %p"), "likes": teste["likes"]} for teste in Post.objects.filter(user__username=self.username).values()],
            "FollowersPosts": [{"user": posts.user.username, "content": posts.content, "timestamp": posts.timestamp.strftime("%b %d %Y, %I:%M %p"), "likes": posts.likes} for posts in Post.objects.filter(user__username__in=FollowersPosts)],
        }
    
class Post(models.Model):
    user = models.ForeignKey("User",on_delete=models.CASCADE, related_name="usersPost")
    content = models.CharField(max_length=255)
    likes = models.ManyToManyField("User", related_name="peaopleliked", blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f" {self.id} {self.user.username} - {self.content}"
    
    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "content": self.content,
            "likes": self.likes,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        }

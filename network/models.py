from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Posts(models.Model):
    content = models.TextField(blank = False)
    likes = models.ManyToManyField(User, related_name="liked_posts")
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "user_posts")
    like = models.IntegerField(default = 0)
    time = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return f"{self.user}: {self.content} @{self.time}. Likes: {self.like}"


class Like(models.Model):
    post = models.ForeignKey(Posts, on_delete = models.CASCADE, related_name = "liked_post")

class Follower(models.Model):
    user_follower = models.ForeignKey(User, blank = True, on_delete = models.CASCADE, related_name = "follows")
    followers = models.ManyToManyField(User, blank = True, related_name = "followers")
    followed = models.ManyToManyField(User, blank = True, related_name = "followed")

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    text = models.TextField(blank=False)
    time = models.DateField(auto_now=True)
    like = models.ManyToManyField(User,blank=True, related_name="like")

    def __str__ (self) -> str:
        return f"{self.id}"

class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post")
    comment = models.TextField(blank=False)
    comment_time = models.DateField(auto_now=True)

    def __str__ (self) -> str:
        return f"{self.id}"

class Follow(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="primary")
    follower = models.ManyToManyField(User, related_name="follower", blank=True)
    follow  = models.ManyToManyField(User, related_name="follow", blank=True)

    def __str__ (self) -> str:
        return f"{self.id}"